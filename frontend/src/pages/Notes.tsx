// src/pages/Notes.tsx

import { useCallback, useEffect, useState } from "react";

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

  const token = localStorage.getItem("token");

  const fetchNotes = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/notes", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (res.ok) {
        setNotes(data.data || []);
      } else {
        console.error(data.msg);
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }, [token]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) {
      fetchNotes();
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (res.ok) {
        setNotes(data.data || []);
      } else {
        console.error(data.msg);
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchNotes();
  }, [fetchNotes]);

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-10">
      <header className="flex flex-col sm:flex-row justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-4 sm:mb-0">我的笔记</h1>
        <div className="flex gap-2">
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:ring-2 focus:ring-red-400 transition"
          >
            退出登录
          </button>
        </div>
      </header>

      <form onSubmit={handleSearch} className="mb-6 flex max-w-md mx-auto">
        <input
          type="text"
          placeholder="Search notes..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 transition"
        >
          Search
        </button>
      </form>

      {loading ? (
        <div className="text-center text-gray-500">加载中...</div>
      ) : notes.length === 0 ? (
        <div className="text-center text-gray-500">暂无笔记</div>
      ) : (
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {notes.map((note) => (
            <div
              key={note.id}
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition"
            >
              <h2 className="text-xl font-semibold text-gray-800">{note.title}</h2>
              <p className="text-gray-600 mt-2 line-clamp-2">{note.summary}</p>
              {note.tags && note.tags.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {note.tags.map((tag) => (
                    <span
                      key={tag.id}
                      className="px-2 py-1 text-xs bg-gray-200 text-gray-700 rounded-full"
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
    </div>
  );
}
