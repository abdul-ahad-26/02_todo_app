"use client";

import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  const { data: session } = authClient.useSession();

  async function handleSignOut() {
    await authClient.signOut();
    router.push("/sign-in");
  }

  return (
    <div className="min-h-screen">
      <nav className="border-b border-border bg-card">
        <div className="mx-auto flex h-14 max-w-4xl items-center justify-between px-4">
          <h1 className="text-lg font-semibold text-foreground">Todo App</h1>
          <div className="flex items-center gap-4">
            {session?.user && (
              <span className="text-sm text-muted">{session.user.name}</span>
            )}
            <button
              onClick={handleSignOut}
              className="rounded-lg px-3 py-1.5 text-sm text-muted transition-colors hover:bg-error/10 hover:text-error"
            >
              Sign Out
            </button>
          </div>
        </div>
      </nav>
      <main className="mx-auto max-w-4xl px-4 py-6">{children}</main>
    </div>
  );
}
