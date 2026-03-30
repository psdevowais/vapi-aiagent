import { Shell } from "@/components/Shell";
import { VoiceInterface } from "@/components/VoiceInterface";

export default function HomePage() {
  return (
    <Shell>
      <div className="mb-6">
        <div className="text-2xl font-semibold">Home</div>
        <div className="mt-1 text-sm text-zinc-600">
          Start a session and view the live conversation.
        </div>
      </div>
      <VoiceInterface />
    </Shell>
  );
}
