// src/api/notes.ts

import api from "./http";


// 请求拦截器：自动带上 token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// 响应拦截器 token失效自动跳转登录页
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // 清理 token
            localStorage.removeItem("token");
            // 跳转到登录页（这里根据你的路由方式调整）
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

// -------------------- 笔记管理 --------------------

// 创建笔记（调用AI生成摘要&标签）
export const createNote = (data: { title: string; content: string }) => {
    return api.post("/notes", data);
};

// 获取笔记列表（分页、标签筛选）
export const getNotes = (params?: { page?: number; size?: number; tag?: string }) => {
    return api.get("/notes", { params });
};

// 查看单条笔记
export const getNoteById = (noteId: number) => {
    return api.get(`/notes/${noteId}`);
};

// 编辑笔记
export const updateNote = (
    noteId: number,
    data: { title?: string; content?: string; tags?: string[] }
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
