from rest_framework import generics

from .models import Lead
from .serializers import LeadSerializer
from .google_sheets import append_lead_row


class LeadListView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def perform_create(self, serializer):
        lead = serializer.save()
        append_lead_row(
            [
                lead.customer_name,
                lead.property_address,
                lead.phone,
                lead.email,
                lead.created_at.isoformat(),
            ]
        )


# Create your views here.
