from rest_framework import serializers
from .models import Candidate


class CandidateUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'resume_file', 'created_at']
        read_only_fields = ['id', 'created_at']

