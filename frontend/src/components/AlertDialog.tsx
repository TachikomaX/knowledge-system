import { useEffect, useState } from "react";
import { X } from "lucide-react";

interface AlertDialogProps {
    isOpen: boolean;
    title: string;
    message: string;
    type?: "success" | "error" | "info";
    autoRedirect?: boolean; // 是否启用倒计时跳转
    redirectSeconds?: number; // 倒计时秒数
    onClose: () => void;
    onRedirect?: () => void; // 倒计时结束后回调（比如跳转）
}

export default function AlertDialog({
    isOpen,
    title,
    message,
    type = "info",
    autoRedirect = false,
    redirectSeconds = 3,
    onClose,
    onRedirect,
}: AlertDialogProps) {
    const [countdown, setCountdown] = useState(redirectSeconds);

    useEffect(() => {
        if (!isOpen || !autoRedirect) return;

        setCountdown(redirectSeconds); // 每次弹窗打开时重置倒计时

        const timer = setInterval(() => {
            setCountdown((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    onRedirect?.(); // 倒计时结束触发跳转
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(timer);
    }, [isOpen, autoRedirect, redirectSeconds, onRedirect]);

    if (!isOpen) return null;

    const colorMap = {
        success: "text-green-600 bg-green-100",
        error: "text-red-600 bg-red-100",
        info: "text-blue-600 bg-blue-100",
    };

    return (
        <div
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={onClose}
        >
            <div
                className="bg-white rounded-xl shadow-xl w-full max-w-sm overflow-hidden animate-fadeIn"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header */}
                <div className={`flex justify-between items-center p-4 border-b ${colorMap[type]}`}>
                    <h3 className="text-lg font-semibold">{title}</h3>
                    <button
                        onClick={onClose}
                        className="text-gray-600 hover:text-gray-800 transition"
                        aria-label="关闭"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Body */}
                <div className="p-4 space-y-2">
                    <p className="text-gray-700">{message}</p>
                    {autoRedirect && countdown > 0 && (
                        <p className="text-sm text-gray-500">
                            {countdown} 秒后即将跳转…
                        </p>
                    )}
                </div>

                {/* Footer */}
                <div className="flex justify-end p-4 border-t bg-gray-50">
                    <button
                        type="button"
                        onClick={onClose}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                    >
                        确定
                    </button>
                </div>
            </div>
        </div>
    );
}
