// src/pages/Notes.tsx

import { useState, useEffect, useCallback } from "react";
import {
  getNotes,
  searchNotes,
  createNote,
  updateNote,
  deleteNote,
} from "../api/notes";
import {
  Menu,
  X,
  FilePlus,
  Search,
  Edit3,
  Trash2,
  LogOut,
} from "lucide-react";

interface Tag {
  id: number;
  name: string;
}

interface Note {
  id: number;
  title: string;
  summary: string;
  tags: Tag[];
  created_at: string;
}

interface NotesProps {
  onLogout: () => void;
}

export default function Notes({ onLogout }: NotesProps) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [query, setQuery] = useState<string>("");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // 获取笔记列表
  const fetchNotes = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getNotes();
      setNotes(res.data.data || []);
    } catch (err) {
      console.error("获取笔记失败:", err);
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

  // 新建笔记
  const handleCreate = async () => {
    const title = prompt("请输入笔记标题：");
    if (!title) return;
    try {
      await createNote({ title, content: "" });
      fetchNotes();
    } catch (err) {
      console.error("创建失败:", err);
    }
  };

  // 编辑笔记
  const handleEdit = async (note: Note) => {
    const newTitle = prompt("修改标题：", note.title);
    if (!newTitle) return;
    try {
      await updateNote(note.id, { title: newTitle, content: note.summary });
      fetchNotes();
    } catch (err) {
      console.error("更新失败:", err);
    }
  };

  // 删除笔记
  const handleDelete = async (id: number) => {
    if (!confirm("确认删除该笔记？")) return;
    try {
      await deleteNote(id);
      fetchNotes();
    } catch (err) {
      console.error("删除失败:", err);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, [fetchNotes]);

  return (
    <div className="flex min-h-screen w-screen">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-16"
        } bg-white border-r border-gray-200 flex flex-col transition-all`}
      >
        <div className="flex items-center justify-between p-4 border-b">
          <span className={`${sidebarOpen ? "block" : "hidden"} font-bold`}>
            知识管理系统
          </span>
          <button onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button className="flex items-center gap-2 p-2 rounded hover:bg-gray-100 w-full text-left">
            📁 {sidebarOpen && "我的笔记"}
          </button>
          <button className="flex items-center gap-2 p-2 rounded hover:bg-gray-100 w-full text-left">
            ⭐ {sidebarOpen && "收藏"}
          </button>
          <button className="flex items-center gap-2 p-2 rounded hover:bg-gray-100 w-full text-left">
            ⚙️ {sidebarOpen && "设置"}
          </button>
        </nav>
        <div className="p-4 border-t">
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
      <main className="flex-1 bg-gray-50 p-6 overflow-y-auto">
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
            className="flex items-center gap-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            <Search size={16} /> 搜索
          </button>
        </form>

        {/* 内容 */}
        {loading ? (
          <div className="text-center text-gray-500">加载中...</div>
        ) : notes.length === 0 ? (
          <div className="text-center text-gray-500">暂无笔记</div>
        ) : (
          <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            {notes.map((note) => (
              <div
                key={note.id}
                className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition"
              >
                <div className="flex justify-between items-start">
                  <h2 className="text-lg font-semibold text-gray-800">
                    {note.title}
                  </h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(note)}
                      className="text-blue-500 hover:text-blue-700"
                    >
                      <Edit3 size={16} />
                    </button>
                    <button
                      onClick={() => handleDelete(note.id)}
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
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
