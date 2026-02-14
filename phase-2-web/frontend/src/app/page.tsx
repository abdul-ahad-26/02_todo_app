"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    async function checkAuth() {
      const { data: session } = await authClient.getSession();
      if (session) {
        router.replace("/dashboard");
      } else {
        router.replace("/sign-in");
      }
    }
    checkAuth();
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="animate-pulse text-muted">Loading...</div>
    </div>
  );
}
