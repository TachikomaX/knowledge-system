import { Heart, Edit3, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";

interface Tag {
    id: number;
    name: string;
}

interface Note {
    id: number;
    title: string;
    content: string;
    summary: string;
    tags: Tag[];
    created_at: string;
    updated_at: string; // 添加更新时间字段
    is_favorited?: boolean; // 添加收藏状态
}

interface NoteCardProps {
    note: Note;
    onEdit: (note: Note) => void;
    onDelete: (id: number) => void;
    onView: (note: Note) => void;
    onToggleFavorite: (id: number) => void;
}

// 格式化时间的辅助函数
const formatTime = (timeString: string): string => {
    const date = new Date(timeString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor(diffMs / (1000 * 60));

    if (diffMinutes < 1) {
        return '刚刚';
    } else if (diffMinutes < 60) {
        return `${diffMinutes}分钟前`;
    } else if (diffHours < 24) {
        return `${diffHours}小时前`;
    } else if (diffDays < 7) {
        return `${diffDays}天前`;
    } else {
        // 返回具体日期，例如 "2025-01-15"
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
    }
};

export default function NoteCard({ note, onEdit, onDelete, onView, onToggleFavorite }: NoteCardProps) {
    const [isFavorite, setIsFavorite] = useState(!!note.is_favorited);

    useEffect(() => {
        setIsFavorite(!!note.is_favorited);
    }, [note.is_favorited]);

    const handleFavoriteClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsFavorite(!isFavorite);
        onToggleFavorite(note.id);
    };

    return (
        <div
            className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition cursor-pointer"
            onClick={() => onView(note)}
        >
            <div className="flex justify-between items-start">
                <h2 className="text-lg font-semibold text-gray-800">
                    {note.title}
                </h2>
                <div className="flex gap-1">
                    {/* 收藏按钮 */}
                    <button
                        onClick={handleFavoriteClick}
                        className={`w-7 h-7 flex items-center justify-center rounded-md hover:text-red-500 transition !bg-transparent !border-none !p-0 ${isFavorite ? 'text-red-500!' : 'text-gray-400'
                            }`}
                    >
                        <Heart size={14} fill={isFavorite ? 'currentColor' : 'none'} />
                    </button>

                    {/* 编辑按钮 */}
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onEdit(note);
                        }}
                        className="w-7 h-7 flex items-center justify-center rounded-md text-blue-500 hover:text-blue-700 !bg-transparent !border-none !p-0"
                    >
                        <Edit3 size={14} />
                    </button>

                    {/* 删除按钮 */}
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onDelete(note.id);
                        }}
                        className="w-7 h-7 flex items-center justify-center rounded-md text-red-500 hover:text-red-700 !bg-transparent !border-none !p-0"
                    >
                        <Trash2 size={14} />
                    </button>
                </div>
            </div>
            <p className="text-gray-600 mt-2 line-clamp-2">
                {note.summary}
            </p>
            {/* 标签和更新时间在同一行 */}
            <div className="mt-3 flex flex-wrap gap-2 items-center">
                {/* 更新时间 */}
                <span className="text-xs text-gray-500 whitespace-nowrap">
                    更新于: {formatTime(note.updated_at)}
                </span>

                {/* 标签 */}
                {note.tags?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                        {note.tags.map((tag) => (
                            <span
                                key={tag.id}
                                className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full"
                            >
                                {tag.name}
                            </span>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}