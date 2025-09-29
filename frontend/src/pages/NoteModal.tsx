// src/pages/NoteModal.tsx

import { useState, useEffect, useRef } from 'react';
import { X } from 'lucide-react';

interface Tag {
  id: number;
  name: string;
}

interface NoteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (note: { title: string; content: string }) => void;
  note?: {
    id: number;
    title: string;
    content: string;
    tags?: Tag[];
  } | null;
  isEditing?: boolean;
}

export default function NoteModal({
  isOpen,
  onClose,
  onSave,
  note = null,
  isEditing = false,
}: NoteModalProps) {
  const [title, setTitle] = useState(note?.title || '');
  const [content, setContent] = useState(note?.content || '');
  const titleRef = useRef<HTMLInputElement>(null);

  // 同步 note 数据（用于编辑）
  useEffect(() => {
    if (note) {
      setTitle(note.title);
      setContent(note.content);
    } else {
      setTitle('');
      setContent('');
    }
  }, [note]);

  // 自动聚焦标题
  useEffect(() => {
    if (isOpen && titleRef.current) {
      titleRef.current.focus();
    }
  }, [isOpen]);

  // ESC 关闭
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSave({ title, content });
  };

  return (
    <div className="fixed inset-0 bg-black/60 bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div
        className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold text-gray-800">
            {isEditing ? '编辑笔记' : note ? '查看笔记' : '新建笔记'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 transition"
            aria-label="关闭"
          >
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-4">
          {/* Title */}
          <div className="mb-4">
            <label htmlFor="note-title" className="block text-sm font-medium text-gray-700 mb-1">
              标题
            </label>
            <input
              id="note-title"
              ref={titleRef}
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="输入笔记标题"
              disabled={!!note && !isEditing}
            />
          </div>

          {/* Content */}
          <div className="mb-4">
            <label htmlFor="note-content" className="block text-sm font-medium text-gray-700 mb-1">
              内容
            </label>
            <textarea
              id="note-content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={8}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              placeholder="写下你的想法..."
              disabled={!!note && !isEditing}
            />
          </div>

          {/* Tags (Optional) */}
          {note?.tags && note.tags.length > 0 && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">标签</label>
              <div className="flex flex-wrap gap-2">
                {note.tags.map((tag) => (
                  <span
                    key={tag.id}
                    className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full"
                  >
                    {tag.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </form>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-4 border-t bg-gray-50">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            取消
          </button>
          {(!note || isEditing) && (
            <button
              type="submit"
              onClick={handleSubmit}
              disabled={!title.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isEditing ? '保存' : '创建'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}