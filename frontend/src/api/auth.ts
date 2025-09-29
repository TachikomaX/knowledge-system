// src/api/auth.ts
import api from "./http";

// 添加拦截器
api.interceptors.response.use(
    (response) => {
        // 如果响应的 code 不为 0，则抛出错误
        if (response.data.code !== 0) {
            const errorMessage = response.data.msg || "未知错误";
            throw new Error(errorMessage);
        }
        return response;
    },
    (error) => {
        // 如果 HTTP 响应码不是 200，抛出错误信息
        const errorMessage = error.response?.data?.msg || error.message || "网络错误";
        throw new Error(errorMessage);
    }
);

export const login = (email: string, password: string) =>
    api.post("/users/login", { email, password });

export const register = (username: string, email: string, password: string) =>
    api.post("/users/register", { username, email, password });
