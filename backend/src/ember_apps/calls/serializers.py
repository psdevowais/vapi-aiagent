from rest_framework import serializers

from .models import AgentSettings, Call, TranscriptEvent
from ember_apps.leads.serializers import LeadSerializer


class TranscriptEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptEvent
        fields = [
            'id',
            'role',
            'text',
            'occurred_at',
            'created_at',
        ]


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = [
            'id',
            'vapi_call_id',
            'status',
            'started_at',
            'ended_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CallListSerializer(CallSerializer):
    transcript_event_count = serializers.IntegerField(read_only=True)
    lead_count = serializers.IntegerField(read_only=True)

    class Meta(CallSerializer.Meta):
        fields = CallSerializer.Meta.fields + [
            'transcript_event_count',
            'lead_count',
        ]


class CallDetailSerializer(CallSerializer):
    transcript_events = TranscriptEventSerializer(many=True, read_only=True)
    leads = LeadSerializer(many=True, read_only=True)

    class Meta(CallSerializer.Meta):
        fields = CallSerializer.Meta.fields + ['transcript_events', 'leads']


class AgentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSettings
        fields = [
            'llm_model',
            'stt_model',
            'tts_model',
            'updated_at',
        ]
