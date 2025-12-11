from django.urls import path
from .views import (
    HealthCheckView,
    CandidateUploadView,
    CandidateDetailView,
    CandidateStatusView,
    CandidateListView,
    DocumentUploadView,
    DocumentRequestView,
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    path('candidates/upload/', CandidateUploadView.as_view(), name='candidate-upload'),
    path('candidates/<int:candidate_id>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('candidates/<int:candidate_id>/status/', CandidateStatusView.as_view(), name='candidate-status'),
    path('candidates/<int:candidate_id>/submit-documents/', DocumentUploadView.as_view(), name='document-upload'),
    path('candidates/<int:candidate_id>/request-documents/', DocumentRequestView.as_view(), name='document-request'),
]
