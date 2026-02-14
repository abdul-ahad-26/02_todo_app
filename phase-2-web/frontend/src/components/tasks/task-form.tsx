"use client";

import { useState } from "react";
import { apiClient, type Task } from "@/lib/api";

interface TaskFormProps {
  userId: string;
  task?: Task;
  onSuccess: () => void;
  onCancel: () => void;
}

export function TaskForm({ userId, task, onSuccess, onCancel }: TaskFormProps) {
  const isEditing = !!task;
  const [title, setTitle] = useState(task?.title ?? "");
  const [description, setDescription] = useState(task?.description ?? "");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError("Title is required.");
      return;
    }
    if (trimmedTitle.length > 200) {
      setError("Title must be 200 characters or fewer.");
      return;
    }
    if (description && description.length > 1000) {
      setError("Description must be 1000 characters or fewer.");
      return;
    }

    setLoading(true);
    try {
      if (isEditing) {
        await apiClient.put(`/api/${userId}/tasks/${task.id}`, {
          title: trimmedTitle,
          description: description || null,
        });
      } else {
        await apiClient.post(`/api/${userId}/tasks`, {
          title: trimmedTitle,
          description: description || null,
        });
      }
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-lg border border-border bg-card p-4 space-y-4"
    >
      <h3 className="text-sm font-medium text-foreground">
        {isEditing ? "Edit Task" : "New Task"}
      </h3>

      {error && (
        <div className="bg-error/10 border border-error/30 text-error rounded-lg px-4 py-3 text-sm">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-1.5">
        <label htmlFor="title" className="text-sm font-medium text-muted">
          Title <span className="text-error">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          maxLength={200}
          placeholder="What needs to be done?"
          className="rounded-lg border border-border bg-background px-4 py-2.5 text-foreground placeholder:text-muted/60 focus:outline-none focus:ring-2 focus:ring-primary/50"
        />
        <span className="text-xs text-muted/60">{title.length}/200</span>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="description" className="text-sm font-medium text-muted">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={1000}
          rows={3}
          placeholder="Add details (optional)"
          className="rounded-lg border border-border bg-background px-4 py-2.5 text-foreground placeholder:text-muted/60 focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none"
        />
        <span className="text-xs text-muted/60">{description.length}/1000</span>
      </div>

      <div className="flex items-center gap-2 justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="rounded-lg px-4 py-2 text-sm text-muted transition-colors hover:bg-border/30"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading
            ? isEditing
              ? "Saving..."
              : "Adding..."
            : isEditing
              ? "Save Changes"
              : "Add Task"}
        </button>
      </div>
    </form>
  );
}
