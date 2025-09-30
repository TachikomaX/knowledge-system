import api from "./http";

// -------------------- 标签管理 --------------------

// 创建标签
export const createTag = (data: { name: string }) => {
    return api.post("/tags", data);
};

// 获取标签列表
export const getTags = (params?: { page?: number; size?: number }) => {
    return api.get("/tags", { params });
};

// 查看单个标签
export const getTagById = (tagId: number) => {
    return api.get(`/tags/${tagId}`);
};

// 更新标签
export const updateTag = (tagId: number, data: { name: string }) => {
    return api.put(`/tags/${tagId}`, data);
};

// 删除标签
export const deleteTag = (tagId: number) => {
    return api.delete(`/tags/${tagId}`);
};