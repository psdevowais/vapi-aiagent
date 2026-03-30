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
            'property_type',
            'bedrooms',
            'bathrooms',
            'occupancy_status',
            'sell_timeline',
            'update_type',
            'additional_notes',
            'phone',
            'email',
            'created_at',
        ]
