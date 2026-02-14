"use client";

import { useState } from "react";
import type { Task } from "@/lib/api";

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
}

export function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  const [toggling, setToggling] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  async function handleToggle() {
    setToggling(true);
    try {
      await onToggle(task.id);
    } finally {
      setToggling(false);
    }
  }

  async function handleDelete() {
    setDeleting(true);
    try {
      await onDelete(task.id);
    } finally {
      setDeleting(false);
      setConfirmDelete(false);
    }
  }

  const createdDate = new Date(task.created_at).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <div className="group flex items-start gap-3 rounded-lg border border-border bg-card p-4 transition-colors hover:border-primary/30">
      <button
        onClick={handleToggle}
        disabled={toggling}
        className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded border border-border transition-colors hover:border-primary disabled:opacity-50"
        aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
      >
        {task.completed && (
          <svg className="h-3.5 w-3.5 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>

      <div className="flex-1 min-w-0">
        <h3
          className={`font-medium text-foreground ${
            task.completed ? "line-through text-muted" : ""
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p className="mt-1 text-sm text-muted line-clamp-2">{task.description}</p>
        )}
        <p className="mt-2 text-xs text-muted/60">{createdDate}</p>
      </div>

      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          onClick={() => onEdit(task)}
          className="rounded p-1.5 text-muted hover:bg-primary/10 hover:text-primary transition-colors"
          aria-label="Edit task"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>

        {confirmDelete ? (
          <div className="flex items-center gap-1">
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="rounded px-2 py-1 text-xs bg-error/10 text-error hover:bg-error/20 transition-colors disabled:opacity-50"
            >
              {deleting ? "..." : "Confirm"}
            </button>
            <button
              onClick={() => setConfirmDelete(false)}
              className="rounded px-2 py-1 text-xs text-muted hover:bg-card transition-colors"
            >
              Cancel
            </button>
          </div>
        ) : (
          <button
            onClick={() => setConfirmDelete(true)}
            className="rounded p-1.5 text-muted hover:bg-error/10 hover:text-error transition-colors"
            aria-label="Delete task"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
