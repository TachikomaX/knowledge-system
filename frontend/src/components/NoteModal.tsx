import { useState, useEffect, useRef } from 'react';
import { X, Tag as TagIcon, Wand2 } from 'lucide-react';
import { getTags, createTag } from '../api/tags';
import { generateSummary } from '../api/notes';


interface Tag {
  id: number;
  name: string;
}

interface NoteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (note: { title: string; content: string; tags?: number[]; summary: string }) => void;
  note?: {
    id: number;
    title: string;
    content: string;
    summary: string;
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
  const [summary, setSummary] = useState(note?.summary || '');

  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);
  const [newTag, setNewTag] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAddingTag, setIsAddingTag] = useState(false);
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const titleRef = useRef<HTMLInputElement>(null);

  // 同步 note 数据（用于编辑）
  useEffect(() => {
    if (note) {
      setTitle(note.title);
      setContent(note.content);
      setSummary(note.summary);
      setSelectedTagIds(note.tags?.map(tag => tag.id) || []);
    } else {
      setTitle('');
      setContent('');
      setSummary('');
      setSelectedTagIds([]);
    }
  }, [note]);

  // 自动聚焦标题
  useEffect(() => {
    if (isOpen && titleRef.current) {
      titleRef.current.focus();
    }
  }, [isOpen]);

  // 加载标签数据
  useEffect(() => {
    if (isOpen) {
      fetchTags();
    }
  }, [isOpen]);

  const fetchTags = async () => {
    try {
      setIsLoading(true);
      const res = await getTags();
      setAvailableTags(res.data.data || []);
    } catch (err) {
      console.error('获取标签失败:', err);
      setAvailableTags([]);
    } finally {
      setIsLoading(false);
    }
  };

  // ESC 关闭
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleTagToggle = (tagId: number) => {
    if (note && !isEditing) return; // 查看模式下不可编辑标签

    setSelectedTagIds(prev =>
      prev.includes(tagId)
        ? prev.filter(id => id !== tagId)
        : [...prev, tagId]
    );
  };

  const handleAddNewTag = async () => {
    if (!newTag.trim()) return;

    // 检查是否已存在同名标签
    if (availableTags.some(tag => tag.name === newTag.trim())) {
      alert('标签已存在');
      return;
    }

    try {
      setIsAddingTag(true);
      // 调用 API 创建新标签
      const res = await createTag({ name: newTag.trim() });
      const createdTag: Tag = res.data.data; // 假设 API 返回格式为 { code: 0, msg: "...", data: { id: ..., name: ... } }

      // 更新可用标签列表
      setAvailableTags(prev => [...prev, createdTag]);
      // 选中新创建的标签
      setSelectedTagIds(prev => [...prev, createdTag.id]);
      // 清空输入框
      setNewTag('');
    } catch (err) {
      console.error('创建标签失败:', err);
      alert('创建标签失败');
    } finally {
      setIsAddingTag(false);
    }
  };

  const handleGenerateSummary = async () => {
    if (!title.trim() || !content.trim()) return;

    try {
      setIsGeneratingSummary(true);
      const res = await generateSummary({ title, content });
      setSummary(res.data.data);
    } catch (err) {
      console.error('生成摘要失败:', err);
    } finally {
      setIsGeneratingSummary(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    onSave({
      title,
      content,
      tags: selectedTagIds,
      summary
    });
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
              <span className="text-red-500 ml-1">*</span>
            </label>
            <input
              id="note-title"
              ref={titleRef}
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${!title.trim() ? 'border-red-500 bg-red-50' : 'border-gray-300'}`}
              placeholder="输入笔记标题"
              disabled={!!note && !isEditing}
            />
          </div>


          {/* Tags */}
          {isEditing && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">标签</label>

              {isLoading ? (
                <div className="text-gray-500 text-sm">加载中...</div>
              ) : (
                <div className="border border-gray-300 rounded-lg p-3">
                  {/* 已选标签显示 */}
                  <div className="mb-3">
                    {selectedTagIds.length > 0 ? (
                      <div className="flex flex-wrap gap-2 mb-2">
                        {availableTags
                          .filter(tag => selectedTagIds.includes(tag.id))
                          .map(tag => (
                            <span
                              key={tag.id}
                              className={`px-2 py-0.5 text-xs rounded-full flex items-center gap-1 ${isEditing
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 text-gray-700'
                                }`}
                            >
                              <TagIcon size={10} />
                              {tag.name}
                              {isEditing && (
                                <button
                                  type="button"
                                  onClick={() => handleTagToggle(tag.id)}
                                  className="ml-1 text-blue-600 hover:text-blue-800"
                                >
                                  ×
                                </button>
                              )}
                            </span>
                          ))}
                      </div>
                    ) : (
                      <p className="text-gray-500 text-sm mb-2">当前笔记未设置标签</p>
                    )}
                  </div>

                  {/* 可选标签列表 */}
                  {isEditing && (
                    <div className="mb-3">
                      <div className="flex flex-wrap gap-2">
                        {availableTags.map(tag => (
                          <button
                            key={tag.id}
                            type="button"
                            onClick={() => handleTagToggle(tag.id)}
                            disabled={selectedTagIds.includes(tag.id)}
                            className={`px-2 py-0.5 text-xs rounded-full flex items-center gap-1 ${selectedTagIds.includes(tag.id)
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                              } ${selectedTagIds.includes(tag.id) ? '' : 'cursor-pointer'}`}
                          >
                            <TagIcon size={12} />
                            {tag.name}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 添加新标签 */}
                  {isEditing && (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={newTag}
                        onChange={(e) => setNewTag(e.target.value)}
                        placeholder="添加新标签"
                        className="flex-1 px-2 py-0.5 border rounded text-xs"
                        onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddNewTag())}
                        disabled={isAddingTag}
                      />
                      <button
                        type="button"
                        onClick={handleAddNewTag}
                        className="px-2 py-0.5 bg-gray-200 rounded text-xs hover:bg-gray-300 disabled:opacity-50"
                        disabled={isAddingTag}
                      >
                        {isAddingTag ? '...' : '+'}
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>)}

          {/* 显示笔记原有标签（查看模式下） */}
          {note && !isEditing && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">标签</label>
              <div className="flex flex-wrap gap-2">
                {note.tags?.map((tag) => (
                  <span
                    key={tag.id}
                    className="px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full flex items-center gap-1"
                  >
                    <TagIcon size={12} />
                    {tag.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Summary */}
          <div className="mb-4">
            <div className="flex justify-between items-center mb-1">
              <label htmlFor="note-summary" className="block text-sm font-medium text-gray-700">
                摘要
              </label>
              {(!note || isEditing) && (
                <button
                  type="button"
                  onClick={handleGenerateSummary}
                  disabled={!title.trim() || !content.trim() || isGeneratingSummary}
                  className="inline-flex items-center px-2 py-0.5 text-xs text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:cursor-not-allowed rounded"
                >
                  <Wand2 size={14} className="mr-1" />
                  {isGeneratingSummary ? '生成中...' : 'AI生成摘要'}
                </button>
              )}
            </div>
            <textarea
              id="note-summary"
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              placeholder="笔记摘要..."
              disabled={!!note && !isEditing}
            />
          </div>

          {/* Content */}
          <div className="mb-4">
            <label htmlFor="note-content" className="block text-sm font-medium text-gray-700 mb-1">
              内容
              <span className="text-red-500 ml-1">*</span>
            </label>
            <textarea
              id="note-content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={8}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${!content.trim() ? 'border-red-500 bg-red-50' : 'border-gray-300'}`}
              placeholder="写下你的想法..."
              disabled={!!note && !isEditing}
            />
            {!content.trim() && (
              <p className="mt-1 text-sm text-red-500">内容不能为空</p>
            )}
          </div>
        </form>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-4 border-t bg-gray-50">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 text-sm text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition"
          >
            取消
          </button>
          {(!note || isEditing) && (
            <button
              type="submit"
              onClick={handleSubmit}
              disabled={!title.trim() || !content.trim()}
              className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isEditing ? '保存' : '创建'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}