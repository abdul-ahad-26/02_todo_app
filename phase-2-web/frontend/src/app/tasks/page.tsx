"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";

interface Task {
  id: string;
  title: string;
  description: string;
  is_complete: boolean;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) {
      router.push("/signin");
      return;
    }
    setToken(storedToken);
    fetchTasks(storedToken);
  }, []);

  const fetchTasks = async (t: string) => {
    try {
      const data = await apiClient.tasks.list(t);
      setTasks(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !token) return;

    try {
      const newTask = await apiClient.tasks.create(
        { title: newTitle, description: newDescription },
        token
      );
      setTasks([...tasks, newTask]);
      setNewTitle("");
      setNewDescription("");
    } catch (err) {
      console.error(err);
    }
  };

  const toggleTask = async (task: Task) => {
    if (!token) return;
    try {
      const updated = await apiClient.tasks.update(
        task.id,
        { is_complete: !task.is_complete },
        token
      );
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)));
    } catch (err) {
      console.error(err);
    }
  };

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
  };

  const saveEdit = async (id: string) => {
    if (!token || !editTitle.trim()) {
      setEditingId(null);
      return;
    }
    try {
      const updated = await apiClient.tasks.update(
        id,
        { title: editTitle, description: editDescription },
        token
      );
      setTasks(tasks.map((t) => (t.id === id ? updated : t)));
      setEditingId(null);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteTask = async (id: string) => {
    if (!token) return;
    try {
      await apiClient.tasks.delete(id, token);
      setTasks(tasks.filter((t) => t.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-foreground">
        Loading tasks...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4 sm:p-8">
      <div className="mx-auto max-w-2xl">
        <header className="mb-8 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-foreground">My Tasks</h1>
          <button
            onClick={() => {
              localStorage.clear();
              router.push("/signin");
            }}
            className="text-sm text-foreground/60 hover:text-error"
          >
            Logout
          </button>
        </header>

        <form onSubmit={addTask} className="mb-8 flex flex-col gap-2">
          <div className="flex gap-2">
            <input
              type="text"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="What needs to be done?"
              className="flex-1 rounded border border-primary/30 bg-slate-900/50 px-4 py-2 text-foreground outline-none focus:border-primary"
            />
            <button
              type="submit"
              className="rounded bg-primary px-6 py-2 font-bold text-white hover:opacity-90"
            >
              Add
            </button>
          </div>
          <textarea
            value={newDescription}
            onChange={(e) => setNewDescription(e.target.value)}
            placeholder="Description (optional)"
            className="w-full rounded border border-primary/10 bg-slate-900/30 px-4 py-2 text-sm text-foreground outline-none focus:border-primary/50"
            rows={2}
          />
        </form>

        <div className="space-y-4">
          {tasks.length === 0 ? (
            <p className="text-center text-foreground/40">No tasks yet. Add one!</p>
          ) : (
            tasks.map((task) => (
              <div
                key={task.id}
                className="flex items-center gap-4 rounded-lg border border-primary/10 bg-slate-900/40 p-4 transition-colors hover:border-primary/30"
              >
                <input
                  type="checkbox"
                  checked={task.is_complete}
                  onChange={() => toggleTask(task)}
                  className="h-5 w-5 cursor-pointer rounded border-primary bg-background accent-secondary"
                />
                <div className="flex-1">
                  {editingId === task.id ? (
                    <div className="flex flex-col gap-2">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && saveEdit(task.id)}
                        autoFocus
                        className="w-full rounded border border-primary/30 bg-slate-900/50 px-2 py-1 text-foreground outline-none focus:border-primary"
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        placeholder="Description (optional)"
                        className="w-full rounded border border-primary/10 bg-slate-900/30 px-2 py-1 text-sm text-foreground outline-none focus:border-primary/50"
                        rows={2}
                      />
                    </div>
                  ) : (
                    <>
                      <h3
                        className={`font-medium ${
                          task.is_complete ? "text-foreground/40 line-through" : "text-foreground"
                        }`}
                      >
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-sm text-foreground/50">{task.description}</p>
                      )}
                    </>
                  )}
                </div>
                {editingId === task.id ? (
                  <button
                    onClick={() => saveEdit(task.id)}
                    className="text-sm font-bold text-primary hover:opacity-80"
                  >
                    Save
                  </button>
                ) : (
                  <button
                    onClick={() => startEditing(task)}
                    className="text-foreground/30 hover:text-primary"
                  >
                    Edit
                  </button>
                )}
                <button
                  onClick={() => deleteTask(task.id)}
                  className="text-foreground/30 hover:text-error"
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
