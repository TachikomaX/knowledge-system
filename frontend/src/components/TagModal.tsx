import { useEffect, useState } from "react";
import { X } from "lucide-react";

interface Tag {
    id: number;
    name: string;
}

interface TagModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: (name: string) => void;
    tag?: Tag | null;
    mode: 'create' | 'edit';
}

export default function TagModal({ isOpen, onClose, onSave, tag, mode }: TagModalProps) {
    const [inputValue, setInputValue] = useState('');

    useEffect(() => {
        if (isOpen && tag) {
            setInputValue(tag.name);
        } else {
            setInputValue('');
        }
    }, [isOpen, tag]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (inputValue.trim()) {
            onSave(inputValue.trim());
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md relative">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
                >
                    <X size={20} />
                </button>

                <h2 className="text-xl font-bold mb-4">
                    {mode === 'create' ? '新建标签' : '编辑标签'}
                </h2>

                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="输入标签名称"
                        className="w-full px-4 py-2 border rounded-lg mb-4"
                        autoFocus
                    />
                    <div className="flex justify-end gap-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 border rounded-lg hover:bg-gray-100"
                        >
                            取消
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        >
                            保存
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}