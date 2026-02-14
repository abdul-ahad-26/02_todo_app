const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api").replace(/\/$/, "");

type FetchOptions = RequestInit & {
  token?: string;
};

async function apiFetch(endpoint: string, options: FetchOptions = {}) {
  const { token, ...rest } = options;
  const headers = new Headers(rest.headers);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  if (!(rest.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...rest,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail?.message || errorData.detail || "API request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const apiClient = {
  tasks: {
    list: (token: string) =>
      apiFetch("/tasks", { token }),

    get: (id: string, token: string) =>
      apiFetch(`/tasks/${id}`, { token }),

    create: (data: { title: string; description?: string }, token: string) =>
      apiFetch("/tasks", {
        method: "POST",
        body: JSON.stringify(data),
        token,
      }),

    update: (id: string, data: { title?: string; description?: string; is_complete?: boolean }, token: string) =>
      apiFetch(`/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
        token,
      }),

    delete: (id: string, token: string) =>
      apiFetch(`/tasks/${id}`, {
        method: "DELETE",
        token,
      }),
  },
};
