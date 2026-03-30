"use client";

import { useEffect, useState } from "react";

import { AgentSettings, getSettings, updateSettings, getGoogleAuthStatus, getGoogleAuthUrl, disconnectGoogle } from "@/lib/api";

export function SettingsClient() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [settings, setSettings] = useState<AgentSettings | null>(null);
  const [googleAuthorized, setGoogleAuthorized] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(true);
  const [googleSigningIn, setGoogleSigningIn] = useState(false);

  useEffect(() => {
    let mounted = true;
    getSettings()
      .then((s) => {
        if (!mounted) return;
        setSettings(s);
        setLoading(false);
      })
      .catch((e) => {
        if (!mounted) return;
        setError(e.message ?? "Failed to load settings");
        setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let mounted = true;
    getGoogleAuthStatus()
      .then((res) => {
        if (!mounted) return;
        setGoogleAuthorized(res.is_authorized);
        setGoogleLoading(false);
      })
      .catch(() => {
        if (!mounted) return;
        setGoogleLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  async function handleGoogleSignIn() {
    setGoogleSigningIn(true);
    try {
      const res = await getGoogleAuthUrl();
      const popup = window.open(
        res.authorization_url,
        "google-auth",
        "width=600,height=700,scrollbars=yes"
      );
      
      const checkClosed = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkClosed);
          getGoogleAuthStatus().then((status) => {
            setGoogleAuthorized(status.is_authorized);
            setGoogleSigningIn(false);
          });
        }
      }, 500);
    } catch {
      setGoogleSigningIn(false);
    }
  }

  async function handleGoogleDisconnect() {
    try {
      await disconnectGoogle();
      setGoogleAuthorized(false);
    } catch {
      // ignore
    }
  }

  async function save() {
    if (!settings) return;
    setSaving(true);
    setError(null);
    try {
      const updated = await updateSettings(settings);
      setSettings(updated);
    } catch (e: any) {
      setError(e?.message ?? "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <div className="text-sm text-zinc-600">Loading…</div>;
  }

  if (error) {
    return <div className="text-sm text-red-600">{error}</div>;
  }

  if (!settings) {
    return <div className="text-sm text-zinc-600">No settings.</div>;
  }

  return (
    <>
    <div className="rounded-xl border border-zinc-200 bg-white">
      <div className="border-b border-zinc-200 px-4 py-3">
        <div className="text-sm font-semibold">Models</div>
        <div className="text-xs text-zinc-500">Update runtime configuration.</div>
      </div>

      <div className="p-4">
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="text-xs font-semibold text-zinc-700">LLM Model</label>
            <input
              value={settings.llm_model}
              onChange={(e) => setSettings({ ...settings, llm_model: e.target.value })}
              className="mt-2 h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm outline-none focus:border-zinc-500"
              placeholder="llama3-8b-8192"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-zinc-700">STT Model</label>
            <select
              value={settings.stt_model}
              onChange={(e) => setSettings({ ...settings, stt_model: e.target.value })}
              className="mt-2 h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm outline-none focus:border-zinc-500"
            >
              <option value="nova-2">nova-2</option>
              <option value="nova-2-general">nova-2-general</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-zinc-700">TTS Model</label>
            <select
              value={settings.tts_model}
              onChange={(e) => setSettings({ ...settings, tts_model: e.target.value })}
              className="mt-2 h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm outline-none focus:border-zinc-500"
            >
              <option value="aura-2">aura-2</option>
              <option value="nova-2">nova-2</option>
            </select>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-between gap-4">
          <div className="text-xs text-zinc-500">
            Changes apply to new messages in the active session.
          </div>
          <button
            onClick={save}
            disabled={saving}
            className="inline-flex h-10 items-center justify-center rounded-lg bg-zinc-900 px-4 text-sm font-semibold text-white disabled:opacity-50"
          >
            {saving ? "Saving…" : "Save"}
          </button>
        </div>
      </div>
    </div>

    <div className="mt-6 rounded-xl border border-zinc-200 bg-white">
      <div className="border-b border-zinc-200 px-4 py-3">
        <div className="text-sm font-semibold">Google Sheets Integration</div>
        <div className="text-xs text-zinc-500">Sync urgent priority leads to Google Sheets.</div>
      </div>

      <div className="p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="text-sm font-medium text-zinc-700">
              {googleLoading ? "Checking status…" : googleAuthorized ? "Connected" : "Not Connected"}
            </div>
            <div className="text-xs text-zinc-500">
              {googleAuthorized
                ? "Urgent leads will automatically sync to Google Sheets"
                : "Sign in to enable Google Sheets sync for urgent leads"}
            </div>
          </div>
          {!googleAuthorized && (
            <button
              onClick={handleGoogleSignIn}
              disabled={googleSigningIn}
              className="inline-flex h-10 items-center justify-center rounded-lg bg-zinc-900 px-4 text-sm font-semibold text-white disabled:opacity-50"
            >
              {googleSigningIn ? "Opening…" : "Sign In with Google"}
            </button>
          )}
          {googleAuthorized && (
            <button
              onClick={handleGoogleDisconnect}
              className="inline-flex h-10 items-center justify-center rounded-lg border border-red-500 bg-red-50 px-4 text-sm font-semibold text-red-700 hover:bg-red-100"
            >
              Disconnect
            </button>
          )}
        </div>
      </div>
    </div>
    </>
  );
}
