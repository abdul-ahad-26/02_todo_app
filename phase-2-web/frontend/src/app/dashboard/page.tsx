"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { TaskList } from "@/components/tasks/task-list";
import { TaskForm } from "@/components/tasks/task-form";
import type { Task } from "@/lib/api";

export default function DashboardPage() {
  const { data: session, isPending } = authClient.useSession();
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function handleTaskCreated() {
    setShowForm(false);
    setRefreshKey((k) => k + 1);
  }

  function handleTaskUpdated() {
    setEditingTask(null);
    setRefreshKey((k) => k + 1);
  }

  function handleEdit(task: Task) {
    setEditingTask(task);
    setShowForm(false);
  }

  if (isPending) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="animate-pulse text-muted">Loading...</div>
      </div>
    );
  }

  if (!session?.user) {
    return null;
  }

  const userId = session.user.id;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-foreground">My Tasks</h2>
        {!showForm && !editingTask && (
          <button
            onClick={() => setShowForm(true)}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary/90"
          >
            Add Task
          </button>
        )}
      </div>

      {showForm && (
        <TaskForm
          userId={userId}
          onSuccess={handleTaskCreated}
          onCancel={() => setShowForm(false)}
        />
      )}

      {editingTask && (
        <TaskForm
          userId={userId}
          task={editingTask}
          onSuccess={handleTaskUpdated}
          onCancel={() => setEditingTask(null)}
        />
      )}

      <TaskList userId={userId} refreshKey={refreshKey} onEdit={handleEdit} />
    </div>
  );
}
