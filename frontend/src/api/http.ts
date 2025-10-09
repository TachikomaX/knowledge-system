// src/api/http.ts
import axios, { AxiosError } from "axios";
import qs from "qs";

const api = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
    paramsSerializer: (params) => {
        // repeat => tag_id_list=2&tag_id_list=3
        return qs.stringify(params, { arrayFormat: "repeat" });
    }
});

// -------------------- 请求拦截器 --------------------
// 自动带上 token
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

// -------------------- 响应拦截器 --------------------
// 处理 code 和 HTTP 状态码
api.interceptors.response.use(
    (response) => {
        // 注意：只处理后端返回的业务错误
        if (response.data.code !== 0) {
            // 这里不能直接 throw，否则 axios 会当作网络错误处理
            return Promise.reject(new Error(response.data.msg || "未知错误"));
        }
        return response;
    },
    (error) => {
        // 统一处理 HTTP 层错误
        if (error.response?.status === 401) {
            // 清理 token
            localStorage.removeItem("token");
            // 跳转到登录页
            window.location.href = "/login";
        }

        const errorMessage =
            error.response?.data?.msg || error.message || "网络错误";
        return Promise.reject(new Error(errorMessage));
    }
);

export default api;

export function getErrorMessage(err: unknown): string {
    if (err instanceof Error) return err.message;
    if ((err as AxiosError).response) {
        return (err as AxiosError<{ msg?: string }>).response?.data?.msg || "请求失败";
    }
    return "未知错误";
}
