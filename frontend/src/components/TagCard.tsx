import React from "react";
import { Edit3, Trash2 } from "lucide-react";

interface Tag {
    id: number;
    name: string;
}

interface TagCardProps {
    tag: Tag;
    onEdit: (tag: Tag) => void;
    onDelete: (id: number) => void;
}

const TagCard: React.FC<TagCardProps> = ({ tag, onEdit, onDelete }) => {
    return (
        <div className="bg-white p-4 rounded-lg shadow flex justify-between items-center ">
            <span className="font-medium text-gray-800">{tag.name}</span>
            <div className="flex gap-2">
                <button
                    onClick={() => onEdit(tag)}
                    className="w-7 h-7 flex items-center justify-center text-blue-500 hover:text-blue-700 !bg-transparent !border-none !p-0"
                >
                    <Edit3 size={16} />
                </button>
                <button
                    onClick={() => onDelete(tag.id)}
                    className="w-7 h-7 flex items-center justify-center text-red-500 hover:text-red-700 !bg-transparent !border-none !p-0"
                >
                    <Trash2 size={16} />
                </button>
            </div>
        </div>
    );
};

export default TagCard;