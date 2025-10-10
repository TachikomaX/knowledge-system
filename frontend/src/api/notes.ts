// src/api/notes.ts

import api from "./http";

// -------------------- 笔记管理 --------------------

// 创建笔记
export const createNote = (data: { title: string; content: string; tags?: string[]; summary?: string }) => {
    return api.post("/notes", data);
};

// 获取笔记列表（分页、标签筛选）
export const getNotes = (params?: { page?: number; size?: number; tag_id_list?: number[] }) => {
    return api.get("/notes", { params });
};

// 查看单条笔记
export const getNoteById = (noteId: number) => {
    return api.get(`/notes/${noteId}`);
};

// 编辑笔记
export const updateNote = (
    noteId: number,
    data: { title?: string; content?: string; tags?: string[]; summary?: string }
) => {
    return api.put(`/notes/${noteId}`, data);
};

// 删除笔记
export const deleteNote = (noteId: number) => {
    return api.delete(`/notes/${noteId}`);
};

// -------------------- 搜索 --------------------

// 全文搜索
export const searchNotes = (query: string) => {
    return api.get("/notes/search", { params: { q: query } });
};

// 语义搜索（向量搜索并生成答案）
export const semanticSearch = (data: { query: string }) => {
    return api.post("/semantic-search", data);
};

// 添加收藏
export const toggleFavoriteNote = (id: number) => {
    return api.post(`/favorites/${id}`);
};

// 移出收藏
export const removeFavoriteNote = (id: number) => {
    return api.delete(`/favorites/${id}`);
};

// 判断笔记是否被收藏
export const checkNotesFavorited = (id: number) => {
    return api.get(`/favorites/${id}/status`);
};

// 获取收藏笔记列表
export const getFavoriteNotes = () => {
    return api.get("/favorites");
};