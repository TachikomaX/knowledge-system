import { X } from "lucide-react";

interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm: () => void;
  onClose: () => void;
  confirmButtonClass?: string;
  cancelButtonClass?: string;
}

export default function ConfirmDialog({
  isOpen,
  title,
  message,
  confirmText = "确认",
  cancelText = "取消",
  onConfirm,
  onClose,
  confirmButtonClass = "px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition",
  cancelButtonClass = "px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition"
}: ConfirmDialogProps) {
  if (!isOpen) return null; // 🚨 不显示时直接返回 null

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden animate-fadeIn"
        onClick={(e) => e.stopPropagation()} // 阻止冒泡，避免点击内容关闭
      >
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 transition"
            aria-label="关闭"
          >
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div className="p-4">
          <p className="text-gray-600">{message}</p>
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-4 border-t bg-gray-50">
          <button type="button" onClick={onClose} className={cancelButtonClass}>
            {cancelText}
          </button>
          <button
            type="button"
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className={confirmButtonClass}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
