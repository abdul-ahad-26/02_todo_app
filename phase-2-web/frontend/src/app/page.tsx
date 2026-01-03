import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground p-4">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl mb-6">
          Evolution of <span className="text-primary">Todo</span>
        </h1>
        <p className="text-xl text-foreground/60 mb-10 leading-relaxed">
          The next step in task management. Experience the Phase II Web application
          built with Next.js, FastAPI, and the Modern High-Contrast theme.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/signup"
            className="rounded-lg bg-primary px-8 py-3 text-lg font-bold text-white transition-all hover:scale-105 active:scale-95 shadow-lg shadow-primary/20"
          >
            Get Started
          </Link>
          <Link
            href="/signin"
            className="rounded-lg border border-secondary/30 bg-secondary/10 px-8 py-3 text-lg font-bold text-secondary transition-all hover:bg-secondary/20 hover:scale-105 active:scale-95"
          >
            Sign In
          </Link>
        </div>
      </div>

      <footer className="absolute bottom-8 text-foreground/30 text-sm">
        Phase II • Constitution v1.2.0 • High-Contrast Dark Theme
      </footer>
    </div>
  );
}
