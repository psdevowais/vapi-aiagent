from django.urls import path

from . import views

urlpatterns = [
    path('calls/', views.CallListCreateView.as_view(), name='call-list-create'),
    path('calls/<uuid:pk>/', views.CallDetailView.as_view(), name='call-detail'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('settings/', views.AgentSettingsView.as_view(), name='agent-settings'),
    path('vapi/webhook/', views.VapiWebhookView.as_view(), name='vapi-webhook'),
]
