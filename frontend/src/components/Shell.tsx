import Link from "next/link";

export function Shell({ children }: { children: React.ReactNode }) {
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
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">{children}</main>
    </div>
  );
}
