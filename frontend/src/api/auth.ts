import { api } from "./client";
import { useAuthStore } from "../store/auth";
import type { ApiResponse, AuthTokens, User } from "../types/api";

export type LoginPayload = {
  email: string;
  password: string;
};

export type RegisterPayload = LoginPayload & {
  name: string;
};

export async function login(payload: LoginPayload): Promise<AuthTokens> {
  const response = await api.post<ApiResponse<AuthTokens>>("/auth/login", payload);
  const data = response.data.data;
  useAuthStore.getState().setSession(data.access_token, data.user);
  return data;
}

export async function register(payload: RegisterPayload): Promise<User> {
  const response = await api.post<ApiResponse<User>>("/auth/register", payload);
  return response.data.data;
}

export async function loadMe(): Promise<User> {
  const response = await api.get<ApiResponse<User>>("/auth/me");
  return response.data.data;
}

export async function logout(): Promise<void> {
  await api.post("/auth/logout");
  useAuthStore.getState().clearSession();
}

