import { API_BASE_URL } from "@/lib/config";

export type CallSummary = {
  id: string;
  created_at: string;
  ended_at: string | null;
  status?: string;
  started_at?: string | null;
  transcript_event_count?: number;
  lead_count?: number;
};

export type CallMessage = {
  id: string;
  role: "user" | "agent";
  content: string;
  created_at: string;
};

export type CallDetail = CallSummary & {
  transcript_events: {
    id: string;
    role: string;
    text: string;
    occurred_at: string | null;
    created_at: string;
  }[];
  leads: {
    id: number;
    call: string | null;
    customer_name: string;
    call_reason: string;
    call_priority: string;
    property_address: string;
    property_type: string;
    bedrooms: string;
    bathrooms: string;
    occupancy_status: string;
    sell_timeline: string;
    update_type: string;
    additional_notes: string;
    phone: string;
    email: string;
    created_at: string;
  }[];
};

export type AnalyticsSummary = {
  total_calls: number;
  calls_by_status: { status: string; count: number }[];
  calls_today?: number;
  calls_by_day?: { day: string; count: number }[];
};

export type AgentSettings = {
  llm_model: string;
  stt_model: string;
  tts_model: string;
};

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }

  return (await res.json()) as T;
}

export function getCalls(): Promise<CallSummary[]> {
  return apiFetch<CallSummary[]>("/calls/");
}

export function getCall(callId: string): Promise<CallDetail> {
  return apiFetch<CallDetail>(`/calls/${callId}/`);
}

export function getAnalytics(): Promise<AnalyticsSummary> {
  return apiFetch<AnalyticsSummary>("/analytics/");
}

export function getSettings(): Promise<AgentSettings> {
  return apiFetch<AgentSettings>("/settings/");
}

export function updateSettings(patch: Partial<AgentSettings>): Promise<AgentSettings> {
  return apiFetch<AgentSettings>("/settings/", {
    method: "PUT",
    body: JSON.stringify(patch),
  });
}
