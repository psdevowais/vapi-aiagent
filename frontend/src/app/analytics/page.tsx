import { BarChart } from "@/components/BarChart";
import { Shell } from "@/components/Shell";
import { getAnalytics } from "@/lib/api";

export default async function AnalyticsPage() {
  const summary = await getAnalytics();

  const callsByDay = summary.calls_by_day ?? [];
  const data = callsByDay.map((d) => ({
    label: d.day,
    value: d.count,
  }));

  const callsToday = summary.calls_today ?? 0;

  return (
    <Shell>
      <div className="mb-6">
        <div className="text-2xl font-semibold">Analytics</div>
        <div className="mt-1 text-sm text-zinc-600">Single-call mode metrics.</div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-xl border border-zinc-200 bg-white p-4">
          <div className="text-xs font-semibold text-zinc-500">Total Calls</div>
          <div className="mt-1 text-2xl font-semibold text-zinc-900">{summary.total_calls}</div>
        </div>
        <div className="rounded-xl border border-zinc-200 bg-white p-4">
          <div className="text-xs font-semibold text-zinc-500">Calls Today</div>
          <div className="mt-1 text-2xl font-semibold text-zinc-900">{callsToday}</div>
        </div>
        <div className="rounded-xl border border-zinc-200 bg-white p-4">
          <div className="text-xs font-semibold text-zinc-500">Mode</div>
          <div className="mt-1 text-2xl font-semibold text-zinc-900">1</div>
        </div>
      </div>

      <div className="mt-6">
        <BarChart data={data} />
      </div>
    </Shell>
  );
}
