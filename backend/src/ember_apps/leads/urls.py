from django.urls import path

from . import views

urlpatterns = [
    path('leads/', views.LeadListView.as_view(), name='lead-list'),
]
