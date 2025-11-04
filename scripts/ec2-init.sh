#!/usr/bin/env bash
set -euo pipefail

# EC2 initialization script for Ubuntu/Debian or Amazon Linux
# - Installs Docker and Docker Compose v2
# - Enables and starts Docker
# - Prepares /opt/kms directory structure
# - Creates .env placeholder if missing
# - Opens firewall (best effort) and prints next steps

GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"; NC="\033[0m"

log() { echo -e "${GREEN}[kms-init]${NC} $*"; }
warn() { echo -e "${YELLOW}[kms-init]${NC} $*"; }
err()  { echo -e "${RED}[kms-init]${NC} $*" 1>&2; }

DISTRO=""
if [ -f /etc/os-release ]; then
  . /etc/os-release
  DISTRO=${ID:-}
fi

log "Detected distro: ${DISTRO:-unknown}"

install_docker_ubuntu() {
  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg lsb-release
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo $UBUNTU_CODENAME) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
}

install_docker_debian() {
  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg lsb-release
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
}

install_docker_amzn() {
  # Amazon Linux 2/2023
  if command -v dnf >/dev/null 2>&1; then
    sudo dnf update -y || true
    sudo dnf install -y docker
  else
    sudo yum update -y || true
    sudo yum install -y docker
  fi
  # Compose plugin via docker CLI v2 may not be in repos; fallback to standalone if missing
  if ! docker compose version >/dev/null 2>&1; then
    warn "docker compose plugin not found, installing standalone compose v2"
    sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
  fi
}

case "$DISTRO" in
  ubuntu)  install_docker_ubuntu ;;
  debian)  install_docker_debian ;;
  amzn|amazon) install_docker_amzn ;;
  *)
    warn "Unknown distro. Attempting generic install..."
    if command -v apt-get >/dev/null 2>&1; then
      install_docker_ubuntu || install_docker_debian || true
    elif command -v yum >/dev/null 2>&1 || command -v dnf >/dev/null 2>&1; then
      install_docker_amzn || true
    else
      err "Cannot determine package manager. Please install Docker manually."
      exit 1
    fi
    ;;
esac

log "Enabling and starting Docker service"
sudo systemctl enable docker || true
sudo systemctl start docker || true

# Add current user to docker group (effect after re-login)
if getent group docker >/dev/null 2>&1; then
  sudo usermod -aG docker "$USER" || true
fi

log "Preparing /opt/kms directory"
sudo mkdir -p /opt/kms
sudo chown -R "$USER":"$USER" /opt/kms

if [ ! -f /opt/kms/.env ]; then
  cat >/opt/kms/.env <<'ENVEOF'
# === Required ===
# Example for AWS RDS (psycopg2 + SQLAlchemy URL)
# DATABASE_URL=postgresql+psycopg2://<user>:<password>@<rds-endpoint>:5432/<db>
DATABASE_URL=
DEEPSEEK_API_KEY=

# Frontend API base (Nginx reverse proxy on same host)
VITE_API_URL=/api

# Whether to expose FastAPI docs in production (default: false)
EXPOSE_DOCS=false
ENVEOF
  log "Created /opt/kms/.env (please fill in values)"
else
  warn "/opt/kms/.env already exists, skipping"
fi

# Best-effort firewall opening (depends on distro)
if command -v ufw >/dev/null 2>&1; then
  warn "Configuring UFW to allow 80/tcp"
  sudo ufw allow 80/tcp || true
  sudo ufw allow 443/tcp || true
elif command -v firewall-cmd >/dev/null 2>&1; then
  warn "Configuring firewalld to allow 80/443"
  sudo firewall-cmd --permanent --add-service=http || true
  sudo firewall-cmd --permanent --add-service=https || true
  sudo firewall-cmd --reload || true
else
  warn "Please ensure EC2 Security Group allows inbound 80/443"
fi

cat <<'NEXT'

============================================================
EC2 init completed.
Next steps:
1) Put your docker-compose.prod.yml to /opt/kms (workflow uploads it automatically)
2) Edit /opt/kms/.env and set DATABASE_URL and DEEPSEEK_API_KEY
3) Ensure your GitHub repository secrets are set:
   - EC2_HOST, EC2_USER, EC2_SSH_KEY
   - GHCR_USERNAME, GHCR_TOKEN (read:packages)
4) Trigger the deploy workflow (push to main/master or manual run)
5) Access your app via http://<EC2_PUBLIC_IP>/
============================================================
NEXT
