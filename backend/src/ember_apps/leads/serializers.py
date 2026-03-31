from rest_framework import serializers

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'call',
            'customer_name',
            'call_reason',
            'call_priority',
            'property_address',
            'occupancy_status',
            'sell_timeline',
            'intent',
            'additional_notes',
            'phone',
            'email',
            'created_at',
        ]
