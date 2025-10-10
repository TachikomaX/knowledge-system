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
    is_favorited?: boolean; // 添加收藏状态
}

interface NoteCardProps {
    note: Note;
    onEdit: (note: Note) => void;
    onDelete: (id: number) => void;
    onView: (note: Note) => void;
    onToggleFavorite: (id: number) => void;
}

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
                    {/* 收藏按钮 - 使用 !important 强制覆盖全局样式 */}
                    <button
                        onClick={handleFavoriteClick}
                        className={`w-7 h-7 flex items-center justify-center rounded-md hover:text-red-500 transition !bg-transparent !border-none !p-0 ${isFavorite ? 'text-red-500!' : 'text-gray-400'
                            }`}
                    >
                        <Heart size={14} fill={isFavorite ? 'currentColor' : 'none'} />
                    </button>

                    {/* 编辑按钮 - 使用 !important 强制覆盖全局样式 */}
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onEdit(note);
                        }}
                        className="w-7 h-7 flex items-center justify-center rounded-md text-blue-500 hover:text-blue-700 !bg-transparent !border-none !p-0"
                    >
                        <Edit3 size={14} />
                    </button>

                    {/* 删除按钮 - 使用 !important 强制覆盖全局样式 */}
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
            {note.tags?.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
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
    );
}