import { useState } from "react";
import { login } from "../api/auth";
import { getErrorMessage } from "../api/http";
import { useNavigate } from "react-router-dom";

interface LoginProps {
  onLogin: () => void;
}

export default function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await login(email, password); // 使用封装好的 login
      const data = res.data;

      if (res.status === 200) {
        localStorage.setItem("token", data.data?.access_token);
        onLogin();
        navigate("/notes"); // 👈 登录成功后跳转
      } else {
        setError(data.msg || "登录失败");
      }
    } catch (err: unknown) {
      console.error(err);
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* 左侧背景图 */}
      <div className="hidden md:block w-2/3 relative">
        <img
          src="/background-1.JPG"
          alt="背景"
          className="object-cover w-full h-full"
        />
        {/* 蒙版 */}
        <div className="absolute inset-0 bg-black/40 bg-opacity-40" />
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <h3 className="text-4xl font-bold text-white drop-shadow-lg">
            你的私人知识管理系统
          </h3>
          <h1 className="text-4xl font-bold text-white drop-shadow-lg mt-4">
            欢迎回来
          </h1>
        </div>
      </div>

      {/* 右侧表单 */}
      <div className="flex flex-1 items-center bg-black/70 justify-center p-6">
        <div className="w-full max-w-md bg-white shadow-lg rounded-xl p-8">
          <h3 className="text-center text-2xl font-bold text-gray-800 mb-6">
            登录到你的账户
          </h3>

          {error && (
            <div className="mb-4 text-sm text-red-600 bg-red-100 p-2 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-gray-700 mb-1" htmlFor="email">
                邮箱
              </label>
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition bg-white text-gray-900 placeholder-gray-400"
                required
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-1" htmlFor="password">
                密码
              </label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition bg-white text-gray-900 placeholder-gray-400"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-2 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 transition mt-8 ${loading ? "opacity-50 cursor-not-allowed" : ""
                }`}
            >
              {loading ? "登录中…" : "登录"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-600">
            没有账号？{" "}
            <a href="/register" className="text-blue-600 hover:underline">
              注册一个
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
