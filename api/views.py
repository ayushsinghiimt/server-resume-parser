from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Candidate
from .serializers import CandidateUploadSerializer


class CandidateUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        serializer = CandidateUploadSerializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            return Response({
                'id': candidate.id,
                'resume_file': request.build_absolute_uri(candidate.resume_file.url),
                'created_at': candidate.created_at,
                'message': 'Resume uploaded successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

