from django.urls import path
from .views import CandidateUploadView

urlpatterns = [
    path('candidates/upload/', CandidateUploadView.as_view(), name='candidate-upload'),
]
