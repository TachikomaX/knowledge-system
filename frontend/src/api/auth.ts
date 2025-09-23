// src/api/auth.ts
import api from "./http";

export const login = (email: string, password: string) =>
    api.post("/login", new URLSearchParams({ username: email, password }));

export const register = (username: string, email: string, password: string) =>
    api.post("/register", { username, email, password });
