import json

from django.utils import timezone

from channels.generic.websocket import AsyncWebsocketConsumer

from ember_apps.leads.google_sheets import append_lead_row, send_urgent_lead_email
from ember_apps.leads.models import Lead

from .models import Call, TranscriptEvent


class TranscriptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.call_id = self.scope["url_route"]["kwargs"]["call_id"]
        self.group_name = f"transcript_{self.call_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def transcript_event(self, event):
        await self.send(text_data=json.dumps(event["payload"]))


class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        call = await Call.objects.acreate(started_at=timezone.now(), status='in_progress')
        self.call_id = str(call.id)
        self.group_name = f"transcript_{self.call_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "type": "session",
                    "call_id": self.call_id,
                }
            )
        )

    async def disconnect(self, close_code):
        await Call.objects.filter(id=self.call_id, ended_at__isnull=True).aupdate(
            ended_at=timezone.now(),
            status='completed',
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                msg = json.loads(text_data)
            except json.JSONDecodeError:
                return

            if msg.get("type") == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))
                return

            if msg.get("type") == "bind" and msg.get("vapi_call_id"):
                vapi_call_id = str(msg.get("vapi_call_id"))
                await Call.objects.filter(id=self.call_id).aupdate(vapi_call_id=vapi_call_id)
                await self.send(text_data=json.dumps({"type": "bound", "call_id": self.call_id}))
                return

            if msg.get("type") == "persist_transcript":
                role = str(msg.get("role") or "unknown")
                text = str(msg.get("text") or "").strip()
                occurred_at_raw = msg.get("occurred_at")
                occurred_at = None
                if isinstance(occurred_at_raw, str) and occurred_at_raw.strip():
                    try:
                        from django.utils.dateparse import parse_datetime

                        occurred_at = parse_datetime(occurred_at_raw)
                    except Exception:
                        occurred_at = None

                if text:
                    await TranscriptEvent.objects.acreate(
                        call_id=self.call_id,
                        role=role,
                        text=text,
                        occurred_at=occurred_at,
                    )
                return

            if msg.get("type") == "persist_lead" and isinstance(msg.get("lead"), dict):
                lead = msg.get("lead") or {}

                customer_name = str(
                    lead.get("caller_name")
                    or lead.get("customer_name")
                    or lead.get("name")
                    or ""
                ).strip()
                phone = str(
                    lead.get("caller_phone")
                    or lead.get("phone")
                    or lead.get("phone_number")
                    or ""
                ).strip()
                email = str(lead.get("caller_email") or lead.get("email") or "").strip()

                if customer_name and phone and email:
                    call_priority = str(lead.get("call_priority") or "").strip()
                    defaults = {
                        "call_reason": str(lead.get("call_reason") or "").strip(),
                        "call_priority": call_priority,
                        "property_address": str(lead.get("property_address") or "").strip(),
                        "property_type": str(lead.get("property_type") or "").strip(),
                        "bedrooms": str(lead.get("bedrooms") or "").strip(),
                        "bathrooms": str(lead.get("bathrooms") or "").strip(),
                        "occupancy_status": str(lead.get("occupancy_status") or "").strip(),
                        "sell_timeline": str(lead.get("sell_timeline") or "").strip(),
                        "update_type": str(lead.get("update_type") or "").strip(),
                        "additional_notes": str(lead.get("additional_notes") or "").strip(),
                    }

                    lead_obj, created = await Lead.objects.aget_or_create(
                        call_id=self.call_id,
                        customer_name=customer_name,
                        phone=phone,
                        email=email,
                        defaults=defaults,
                    )
                    if created and call_priority.lower() == "urgent":
                        import asyncio
                        await asyncio.to_thread(
                            append_lead_row,
                            [
                                lead_obj.customer_name,
                                lead_obj.property_address,
                                lead_obj.phone,
                                lead_obj.email,
                                lead_obj.call_priority,
                                lead_obj.created_at.isoformat(),
                            ],
                        )
                        await asyncio.to_thread(
                            send_urgent_lead_email,
                            {
                                'customer_name': lead_obj.customer_name,
                                'phone': lead_obj.phone,
                                'email': lead_obj.email,
                                'property_address': lead_obj.property_address,
                                'call_priority': lead_obj.call_priority,
                            },
                        )
                return

        if bytes_data:
            return

    async def transcript_event(self, event):
        payload = event.get("payload") or {}
        await self.send(
            text_data=json.dumps(
                {
                    "type": "transcript_event",
                    **payload,
                }
            )
        )
