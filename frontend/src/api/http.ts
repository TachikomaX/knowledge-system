// src/api/http.ts
import axios, { AxiosError } from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

export default api;

export function getErrorMessage(err: unknown): string {
    if (err instanceof Error) return err.message;
    if ((err as AxiosError).response) {
        return (err as AxiosError<{ msg?: string }>).response?.data?.msg || "请求失败";
    }
    return "未知错误";
}
