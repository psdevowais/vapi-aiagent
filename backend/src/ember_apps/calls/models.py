import uuid

from django.db import models


class Call(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    vapi_call_id = models.CharField(max_length=128, blank=True, default='')
    status = models.CharField(max_length=32, blank=True, default='')
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class TranscriptEvent(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='transcript_events')
    role = models.CharField(max_length=32)
    text = models.TextField()
    occurred_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class AgentSettings(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    llm_model = models.CharField(max_length=128, default='')
    stt_model = models.CharField(max_length=128, default='')
    tts_model = models.CharField(max_length=128, default='')
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
