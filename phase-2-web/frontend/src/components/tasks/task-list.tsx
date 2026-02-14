"use client";

import { useCallback, useEffect, useState } from "react";
import { apiClient, type Task } from "@/lib/api";
import { TaskItem } from "./task-item";
import { EmptyState } from "./empty-state";

interface TaskListProps {
  userId: string;
  refreshKey: number;
  onEdit: (task: Task) => void;
}

export function TaskList({ userId, refreshKey, onEdit }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await apiClient.get<Task[]>(`/api/${userId}/tasks`);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks.");
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks, refreshKey]);

  async function handleToggle(taskId: string) {
    try {
      const updated = await apiClient.patch<Task>(
        `/api/${userId}/tasks/${taskId}/complete`
      );
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? updated : t))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to toggle task.");
    }
  }

  async function handleDelete(taskId: string) {
    try {
      await apiClient.del(`/api/${userId}/tasks/${taskId}`);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task.");
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col gap-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="h-20 animate-pulse rounded-lg border border-border bg-card"
          />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-error/10 border border-error/30 text-error rounded-lg px-4 py-3 text-sm">
        {error}
        <button
          onClick={fetchTasks}
          className="ml-2 underline hover:no-underline"
        >
          Retry
        </button>
      </div>
    );
  }

  if (tasks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="flex flex-col gap-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={handleToggle}
          onEdit={onEdit}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}
