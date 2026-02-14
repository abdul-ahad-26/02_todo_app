export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="text-5xl mb-4">
        <span role="img" aria-label="clipboard">📋</span>
      </div>
      <h3 className="text-lg font-medium text-foreground mb-2">
        No tasks yet
      </h3>
      <p className="text-sm text-muted max-w-xs">
        Create your first task to get started. Click the &quot;Add Task&quot; button above.
      </p>
    </div>
  );
}
