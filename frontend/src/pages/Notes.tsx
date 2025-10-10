// src/pages/Notes.tsx

import { useState, useEffect, useCallback, useRef } from "react";
import {
  getNotes,
  searchNotes,
  createNote,
  updateNote,
  deleteNote,
  toggleFavoriteNote,
  removeFavoriteNote,
} from "../api/notes";
import { getTags, createTag, updateTag, deleteTag } from "../api/tags";
import {
  Menu,
  X,
  FilePlus,
  Search,
  Edit3,
  Trash2,
  LogOut,
  Plus,
  Tag as TagIcon,
} from "lucide-react";
import NoteModal from "../components/NoteModal";
import ConfirmDialog from "../components/ConfirmDialog";
import TagModal from "../components/TagModal";
import NoteCard from "../components/NoteCard";

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
  is_favorited?: boolean; // 收藏状态
}

interface NotesProps {
  onLogout: () => void;
}

export default function Notes({ onLogout }: NotesProps) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [query, setQuery] = useState<string>("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeView, setActiveView] = useState<'notes' | 'tags'>('notes');

  // 笔记相关状态
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentNote, setCurrentNote] = useState<Note | null>(null);
  const [modalMode, setModalMode] = useState<'create' | 'view' | 'edit'>('create');
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    onConfirm: () => void;
    message: string;
  }>({
    isOpen: false,
    onConfirm: () => { },
    message: "",
  });

  // 标签管理相关状态
  const [isTagModalOpen, setIsTagModalOpen] = useState(false);
  const [currentTag, setCurrentTag] = useState<Tag | null>(null);
  const [tagModalMode, setTagModalMode] = useState<'create' | 'edit'>('create');
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]); // 多选标签ID数组
  const [isTagDropdownOpen, setIsTagDropdownOpen] = useState(false);
  const tagDropdownRef = useRef<HTMLDivElement>(null);
  const [tagsLoaded, setTagsLoaded] = useState(false);



  const fetchNotesByTags = useCallback(async (tagIds: number[] = []) => {
    setLoading(true);
    try {
      const res = await getNotes({ tag_id_list: tagIds });
      setNotes(res.data.data || []);
    } catch (err) {
      console.error("获取笔记失败:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  // 获取笔记列表
  const fetchNotes = useCallback(async () => {
    await fetchNotesByTags(selectedTagIds);
  }, [selectedTagIds, fetchNotesByTags]);

  // 获取标签列表
  const fetchTags = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getTags();
      setTags(res.data.data || []);
    } catch (err) {
      console.error("获取标签失败:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  // 搜索
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) {
      fetchNotes();
      return;
    }
    setLoading(true);
    try {
      const res = await searchNotes(query);
      setNotes(res.data.data || []);
    } catch (err) {
      console.error("搜索失败:", err);
    } finally {
      setLoading(false);
    }
  };

  // 获取标签并打开下拉
  const handleTagDropdownToggle = async () => {
    if (!isTagDropdownOpen && !tagsLoaded) {
      await fetchTags();
      setTagsLoaded(true);
    }
    setIsTagDropdownOpen(prev => !prev);
  };

  // 选择标签时即时生效（
  const handleTagSelection = (tagId: number, isChecked: boolean) => {
    setSelectedTagIds(prev => {
      const newSelected = isChecked ? (prev.includes(tagId) ? prev : [...prev, tagId]) : prev.filter(id => id !== tagId);
      // 直接用 newSelected 发起请求（即时生效）
      fetchNotesByTags(newSelected);
      return newSelected;
    });
  };

  // 笔记相关函数
  const handleCreate = () => {
    setCurrentNote(null);
    setModalMode('create');
    setIsModalOpen(true);
  };

  const handleView = (note: Note) => {
    setCurrentNote(note);
    setModalMode('view');
    setIsModalOpen(true);
  };

  const handleEdit = (note: Note) => {
    setCurrentNote(note);
    setModalMode('edit');
    setIsModalOpen(true);
  };

  const handleDelete = (id: number) => {
    setConfirmDialog({
      isOpen: true,
      message: "确认删除该笔记？此操作不可撤销。",
      onConfirm: async () => {
        try {
          await deleteNote(id);
          fetchNotes();
        } catch (err) {
          console.error("删除失败:", err);
        }
      },
    });
  };

  // 标签管理相关函数
  const handleCreateTag = () => {
    setCurrentTag(null);
    setTagModalMode('create');
    setIsTagModalOpen(true);
  };

  const handleEditTag = (tag: Tag) => {
    setCurrentTag(tag);
    setTagModalMode('edit');
    setIsTagModalOpen(true);
  };

  const handleDeleteTag = (id: number) => {
    setConfirmDialog({
      isOpen: true,
      message: "确认删除该标签？此操作不可撤销。",
      onConfirm: async () => {
        try {
          await deleteTag(id);
          fetchTags();
        } catch (err) {
          console.error("删除标签失败:", err);
        }
      },
    });
  };

  const handleSaveTag = async (name: string) => {
    try {
      if (tagModalMode === 'create') {
        await createTag({ name });
      } else if (currentTag) {
        await updateTag(currentTag.id, { name });
      }
      fetchTags();
      setIsTagModalOpen(false);
    } catch (err) {
      console.error(tagModalMode === 'create' ? '创建标签失败' : '更新标签失败', err);
    }
  };

  const handleToggleFavorite = async (id: number) => {
    try {
      // 获取当前笔记
      const currentNote = notes.find(note => note.id === id);
      if (!currentNote) return;

      if (currentNote.is_favorited) {
        // 如果当前是收藏状态，则移出收藏
        await removeFavoriteNote(id);
      } else {
        // 如果当前不是收藏状态，则添加收藏
        await toggleFavoriteNote(id);
      }

      // 更新本地状态 - 只翻转当前笔记的收藏状态
      setNotes(prevNotes =>
        prevNotes.map(note =>
          note.id === id
            ? { ...note, is_favorite: !note.is_favorited }
            : note
        )
      );
    } catch (error) {
      console.error("切换收藏状态失败:", error);
      // 如果API调用失败，不更新本地状态
    }
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (tagDropdownRef.current && !tagDropdownRef.current.contains(event.target as Node)) {
        setIsTagDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (activeView === 'notes') {
      fetchNotes();
    } else {
      fetchTags();
    }
  }, [activeView, fetchNotes, fetchTags]);

  return (
    <div className="flex min-h-screen w-screen relative overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`${sidebarOpen ? "w-64" : "w-16"
          } bg-white border-r border-gray-200 flex flex-col transition-all`}
      >
        <div className="flex items-center justify-between p-4 border-b-1 border-gray-200">
          <span className={`${sidebarOpen ? "block" : "hidden"} font-bold`}>
            知识管理系统
          </span>
          <button onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => setActiveView('notes')}
            className={`flex items-center gap-2 p-2 rounded hover:bg-gray-100 w-full text-left ${activeView === 'notes' ? 'bg-blue-50 text-blue-600' : ''}`}
          >
            📁 {sidebarOpen && "我的笔记"}
          </button>
          <button className="flex items-center gap-2 p-2 rounded hover:bg-gray-100 w-full text-left">
            ⭐ {sidebarOpen && "收藏"}
          </button>
          <button
            onClick={() => setActiveView('tags')}
            className={`flex items-center gap-2 p-2 rounded hover:bg-gray-100 w-full text-left ${activeView === 'tags' ? 'bg-blue-50 text-blue-600' : ''}`}
          >
            <TagIcon size={16} /> {sidebarOpen && "标签管理"}
          </button>
        </nav>
        <div className="p-4 border-t-1 border-gray-200">
          <button
            onClick={onLogout}
            className="flex items-center gap-2 w-full p-2 rounded hover:bg-red-50 text-red-600"
          >
            <LogOut size={16} />
            {sidebarOpen && "退出登录"}
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 bg-gray-100 p-6 overflow-y-auto">
        {activeView === 'notes' ? (
          <>
            <header className="flex flex-col sm:flex-row justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-800">我的笔记</h1>
              <button
                onClick={handleCreate}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              >
                <FilePlus size={18} />
                新建笔记
              </button>
            </header>

            {/* 搜索 */}
            <form
              onSubmit={handleSearch}
              className="flex items-center gap-2 mb-6 max-w-md"
            >
              <input
                type="text"
                placeholder="搜索笔记..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="submit"
                className="flex items-center gap-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition whitespace-nowrap flex-shrink-0"
              >
                <Search size={16} /> 搜索
              </button>

              {/* 多选标签筛选器 */}
              <div ref={tagDropdownRef} className="relative">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={handleTagDropdownToggle}
                    className="px-4 py-2 border border-gray-300 rounded-lg flex items-center gap-2 hover:bg-gray-50 transition whitespace-nowrap"
                  >
                    <TagIcon size={16} />
                    {selectedTagIds.length > 0 ? `${selectedTagIds.length}个标签` : "标签筛选"}
                    <svg
                      className={`w-4 h-4 transition-transform ${isTagDropdownOpen ? 'rotate-180' : ''}`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {/* 若有已选标签，显示一个小清除按钮，一键清空 */}
                  {selectedTagIds.length > 0 && (
                    <button
                      type="button"
                      onClick={() => { setSelectedTagIds([]); fetchNotes(); }}
                      className="px-3 py-2 rounded-md text-sm bg-gray-100 hover:bg-gray-200 transition whitespace-nowrap"
                      aria-label="清除标签筛选"
                    >
                      清除已选标签
                    </button>
                  )}
                </div>

                {isTagDropdownOpen && (
                  <div className="absolute right-0 mt-1 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
                    {loading && tags.length === 0 ? (
                      <div className="p-3 text-center text-gray-500">加载中...</div>
                    ) : (
                      <div className="max-h-48 overflow-y-auto">
                        {tags.map(tag => (
                          <div key={tag.id} className="px-3 py-1 hover:bg-gray-50">
                            <label className="flex items-center cursor-pointer select-none">
                              <input
                                type="checkbox"
                                checked={selectedTagIds.includes(tag.id)}
                                onChange={(e) => handleTagSelection(tag.id, e.target.checked)}
                                className="mr-2"
                              />
                              <span className="text-sm">{tag.name}</span>
                            </label>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

            </form>

            {/* 内容 */}
            {loading ? (
              <div className="text-center text-gray-500">加载中...</div>
            ) : notes.length === 0 ? (
              <div className="text-center text-gray-500">暂无笔记</div>
            ) : (
              <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {notes.map((note) => (
                  <NoteCard
                    key={note.id}
                    note={note}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onView={handleView}
                    onToggleFavorite={handleToggleFavorite}
                  />
                ))}
              </div>
            )}
          </>
        ) : (
          // 标签管理视图
          <div>
            <header className="flex flex-col sm:flex-row justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-800">标签管理</h1>
              <button
                onClick={handleCreateTag}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              >
                <Plus size={18} />
                新建标签
              </button>
            </header>

            {loading ? (
              <div className="text-center text-gray-500">加载中...</div>
            ) : tags.length === 0 ? (
              <div className="text-center text-gray-500">暂无标签</div>
            ) : (
              <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                {tags.map((tag) => (
                  <div
                    key={tag.id}
                    className="bg-white p-4 rounded-lg shadow flex justify-between items-center"
                  >
                    <span className="font-medium text-gray-800">{tag.name}</span>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleEditTag(tag)}
                        className="text-blue-500 hover:text-blue-700"
                      >
                        <Edit3 size={16} />
                      </button>
                      <button
                        onClick={() => handleDeleteTag(tag.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      {/* 笔记编辑弹窗 */}
      <NoteModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={async (data) => {
          try {
            if (modalMode === 'create') {
              await createNote({ ...data, tags: data.tags?.map(String) });
            } else if (modalMode === 'edit' && currentNote) {
              await updateNote(currentNote.id, { ...data, tags: data.tags?.map(String) });
            }
            fetchNotes();
            setIsModalOpen(false);
          } catch (err) {
            console.error(modalMode === 'create' ? '创建失败' : '更新失败', err);
          }
        }}
        note={currentNote}
        isEditing={modalMode !== 'view'}
      />

      {/* 标签编辑弹窗 */}
      <TagModal
        isOpen={isTagModalOpen}
        onClose={() => setIsTagModalOpen(false)}
        onSave={handleSaveTag}
        tag={currentTag}
        mode={tagModalMode}
      />

      {/* 确认弹窗 */}
      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        title="确认操作"
        onClose={() => setConfirmDialog(prev => ({ ...prev, isOpen: false }))}
        onConfirm={confirmDialog.onConfirm}
        message={confirmDialog.message}
        confirmText="删除"
        confirmButtonClass="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
      />
    </div>
  );
}