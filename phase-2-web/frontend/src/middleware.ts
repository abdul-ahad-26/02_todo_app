import { NextRequest, NextResponse } from "next/server";
import { getSessionCookie } from "better-auth/cookies";

export function middleware(request: NextRequest) {
  const session = getSessionCookie(request);
  const isAuthPage = ["/signin", "/signup"].some((p) =>
    request.nextUrl.pathname.startsWith(p),
  );

  if (!session && !isAuthPage) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }

  if (session && isAuthPage) {
    return NextResponse.redirect(new URL("/tasks", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/tasks/:path*", "/signin", "/signup"],
};
