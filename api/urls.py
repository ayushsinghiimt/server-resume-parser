from django.urls import path
from .views import (
    CandidateUploadView,
    CandidateDetailView,
    CandidateStatusView,
    CandidateListView,
    DocumentUploadView,
)

urlpatterns = [
    path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    path('candidates/upload/', CandidateUploadView.as_view(), name='candidate-upload'),
    path('candidates/<int:candidate_id>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('candidates/<int:candidate_id>/status/', CandidateStatusView.as_view(), name='candidate-status'),
    path('candidates/<int:candidate_id>/submit-documents/', DocumentUploadView.as_view(), name='document-upload'),
]
