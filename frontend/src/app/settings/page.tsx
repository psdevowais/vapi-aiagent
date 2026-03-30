import { Shell } from "@/components/Shell";
import { SettingsClient } from "@/app/settings/SettingsClient";

export default function SettingsPage() {
  return (
    <Shell>
      <div className="mb-6">
        <div className="text-2xl font-semibold">Settings</div>
        <div className="mt-1 text-sm text-zinc-600">Update STT/TTS/LLM configuration.</div>
      </div>

      <SettingsClient />
    </Shell>
  );
}
