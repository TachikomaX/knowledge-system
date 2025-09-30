import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth";
import { getErrorMessage } from "../api/http";
import AlertDialog from "../components/AlertDialog";

export default function Register() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isAlertOpen, setAlertOpen] = useState(false);
    const [alertInfo, setAlertInfo] = useState({ title: "", message: "", type: "info" as "success" | "error" | "info" });



    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            await register(username, email, password);
            setAlertInfo({
                title: "注册成功",
                message: "欢迎加入！现在可以登录了。",
                type: "success",
            });
            setAlertOpen(true);
        } catch (err: unknown) {
            console.error(err);
            setError(getErrorMessage(err));
            setAlertInfo({
                title: "注册失败",
                message: getErrorMessage(err) || "发生了未知错误，请稍后再试。",
                type: "error",
            });
            setAlertOpen(true);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <img
                src="/background-1.JPG"
                alt="背景"
                className="absolute inset-0 w-full h-full object-cover"
            />
            {/* 蒙版 */}
            <div className="absolute inset-0 bg-black/40 bg-opacity-40" />
            <div className="relative z-10 bg-white /90 backdrop-blur-md p-6 rounded-lg shadow-lg w-full max-w-sm">
                <h1 className="text-2xl font-bold mb-4 text-center">注册</h1>
                <form onSubmit={handleRegister} className="space-y-4">
                    <input
                        type="text"
                        placeholder="用户名"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        type="email"
                        placeholder="邮箱"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        type="password"
                        placeholder="密码"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
                    >
                        {loading ? "注册中..." : "注册"}
                    </button>
                    {error && (
                        <div className="mb-4 text-sm text-red-600 bg-red-100 p-2 rounded">
                            {error}
                        </div>
                    )}
                </form>
                <p className="mt-4 text-center text-sm text-gray-600">
                    已有账号？
                    <a href="/login" className="text-blue-600 hover:underline">
                        去登录
                    </a>
                </p>
            </div>

            <AlertDialog
                isOpen={isAlertOpen}
                title={alertInfo.title}
                message={alertInfo.message}
                type={alertInfo.type}
                autoRedirect={alertInfo.type === "success"} // 成功时才倒计时跳转
                redirectSeconds={5}
                onClose={() => setAlertOpen(false)}
                onRedirect={() => navigate("/login")} // 倒计时结束跳转到登录页
            />
        </div>
    );
}
