from django.db import models


class Lead(models.Model):
    call = models.ForeignKey(
        'calls.Call',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
    )
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=64)
    email = models.EmailField()
    call_reason = models.CharField(max_length=32, blank=True, default='')
    call_priority = models.CharField(max_length=32, blank=True, default='')
    property_address = models.TextField(blank=True, default='')
    property_type = models.CharField(max_length=32, blank=True, default='')
    bedrooms = models.CharField(max_length=32, blank=True, default='')
    bathrooms = models.CharField(max_length=32, blank=True, default='')
    occupancy_status = models.CharField(max_length=32, blank=True, default='')
    sell_timeline = models.CharField(max_length=128, blank=True, default='')
    update_type = models.CharField(max_length=64, blank=True, default='')
    additional_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

# Create your models here.
