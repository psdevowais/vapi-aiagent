'use client';

import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";

export function Shell({ children }: { children: React.ReactNode }) {
  const { user, logout, loading } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-zinc-50 flex items-center justify-center">
        <div className="text-zinc-600">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-md bg-zinc-900" />
            <div>
              <div className="text-sm font-semibold leading-4">Ember Homes</div>
              <div className="text-xs text-zinc-500">Voice Agent Dashboard</div>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <nav className="flex items-center gap-6 text-sm font-medium text-zinc-700">
              <Link className="hover:text-zinc-900" href="/">
                Home
              </Link>
              <Link className="hover:text-zinc-900" href="/calls">
                Calls
              </Link>
              <Link className="hover:text-zinc-900" href="/analytics">
                Analytics
              </Link>
              <Link className="hover:text-zinc-900" href="/settings">
                Settings
              </Link>
            </nav>
            <div className="flex items-center gap-3 pl-6 border-l border-zinc-200">
              <div className="text-sm">
                <span className="font-medium text-zinc-900">{user.username}</span>
              </div>
              <button
                onClick={handleLogout}
                className="text-sm text-zinc-600 hover:text-zinc-900 transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">{children}</main>
    </div>
  );
}
