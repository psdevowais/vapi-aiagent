from django.urls import path

from . import views
from .oauth_views import GoogleAuthorizeView, GoogleAuthStatusView, GoogleCallbackView, GoogleDisconnectView

urlpatterns = [
    path('leads/', views.LeadListView.as_view(), name='lead-list'),
    path('auth/google/', GoogleAuthorizeView.as_view(), name='google-authorize'),
    path('auth/google/callback/', GoogleCallbackView.as_view(), name='google-callback'),
    path('auth/google/status/', GoogleAuthStatusView.as_view(), name='google-auth-status'),
    path('auth/google/disconnect/', GoogleDisconnectView.as_view(), name='google-disconnect'),
]
