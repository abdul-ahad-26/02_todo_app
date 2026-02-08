import { authClient } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function getAuthHeaders(): Promise<HeadersInit> {
  const { data, error } = await authClient.token();

  if (error || !data?.token) {
    throw new Error("AUTH_REQUIRED");
  }

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${data.token}`,
  };
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = await getAuthHeaders();
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { ...headers, ...options.headers },
  });

  if (res.status === 401) {
    throw new Error("AUTH_REQUIRED");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }

  return res.json();
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateInput {
  title: string;
  description?: string;
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  is_complete?: boolean;
}

export const apiClient = {
  tasks: {
    list: () => request<Task[]>("/tasks"),

    create: (data: TaskCreateInput) =>
      request<Task>("/tasks", {
        method: "POST",
        body: JSON.stringify(data),
      }),

    get: (id: string) => request<Task>(`/tasks/${id}`),

    update: (id: string, data: TaskUpdateInput) =>
      request<Task>(`/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),

    toggleComplete: (id: string) =>
      request<Task>(`/tasks/${id}/complete`, {
        method: "PATCH",
      }),

    delete: (id: string) =>
      request<{ message: string }>(`/tasks/${id}`, {
        method: "DELETE",
      }),
  },
};
