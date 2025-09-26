// src/api/auth.ts
import api from "./http";

export const login = (email: string, password: string) =>
    api.post("/users/login", { email, password });

export const register = (username: string, email: string, password: string) =>
    api.post("/users/register", { username, email, password });
