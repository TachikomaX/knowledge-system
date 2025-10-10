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
                <div className="flex gap-2">
                    <button
                        onClick={handleFavoriteClick}
                        className={`hover:text-red-500 transition ${isFavorite ? 'text-red-500!' : 'text-gray-400'
                            }`}
                    >
                        <Heart size={16} fill={isFavorite ? 'currentColor' : 'none'} />
                    </button>
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onEdit(note);
                        }}
                        className="text-blue-500 hover:text-blue-700"
                    >
                        <Edit3 size={16} />
                    </button>
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onDelete(note.id);
                        }}
                        className="text-red-500 hover:text-red-700"
                    >
                        <Trash2 size={16} />
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