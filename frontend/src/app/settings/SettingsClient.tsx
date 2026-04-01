"use client";

import { useEffect, useState } from "react";

import { getGoogleAuthStatus, getGoogleAuthUrl, disconnectGoogle } from "@/lib/api";

export function SettingsClient() {
  const [googleAuthorized, setGoogleAuthorized] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(true);
  const [googleSigningIn, setGoogleSigningIn] = useState(false);

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

  if (googleLoading) {
    return <div className="text-sm text-zinc-600">Loading…</div>;
  }

  return (
    <div className="rounded-xl border border-zinc-200 bg-white">
      <div className="border-b border-zinc-200 px-4 py-3">
        <div className="text-sm font-semibold">Google Authentication for Sheets and Gmail</div>
        <div className="text-xs text-zinc-500">Sync urgent priority leads to Google Sheets and send emails via Gmail.</div>
      </div>

      <div className="p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="text-sm font-medium text-zinc-700">
              {googleAuthorized ? "Connected" : "Not Connected"}
            </div>
            <div className="text-xs text-zinc-500">
              {googleAuthorized
                ? "Leads will automatically sync to Google Sheets"
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
  );
}
