import logging
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Candidate
from .serializers import (
    CandidateUploadSerializer,
    CandidateDetailSerializer,
)
from .services.resume_parser import ResumeParserService

logger = logging.getLogger(__name__)


class CandidateUploadView(APIView):
    """Upload resume and trigger parsing."""
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        serializer = CandidateUploadSerializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            
            # Parse the resume using LangChain
            try:
                parser_service = ResumeParserService()
                parsed_data = parser_service.parse_resume(candidate)
                parser_service.save_to_database(candidate, parsed_data)
                
                # Refresh candidate to get updated data
                candidate.refresh_from_db()
                
                return Response({
                    'id': candidate.id,
                    'resume_file': request.build_absolute_uri(candidate.resume_file.url),
                    'created_at': candidate.created_at,
                    'parsing_status': candidate.parsing_status,
                    'message': 'Resume uploaded and parsed successfully',
                    'candidate_url': request.build_absolute_uri(f'/api/candidates/{candidate.id}/')
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                error_msg = str(e)
                error_traceback = traceback.format_exc()
                logger.error(f"Error parsing resume: {error_msg}")
                logger.error(f"Full traceback:\n{error_traceback}")
                print(f"ERROR PARSING RESUME: {error_msg}")
                print(f"FULL TRACEBACK:\n{error_traceback}")
                return Response({
                    'id': candidate.id,
                    'resume_file': request.build_absolute_uri(candidate.resume_file.url),
                    'created_at': candidate.created_at,
                    'parsing_status': 'failed',
                    'error': error_msg,
                    'message': 'Resume uploaded but parsing failed'
                }, status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateDetailView(APIView):
    """Retrieve detailed candidate information."""
    
    def get(self, request, candidate_id, format=None):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            serializer = CandidateDetailSerializer(candidate, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            return Response(
                {'error': 'Candidate not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class CandidateStatusView(APIView):
    """Check parsing status of a candidate."""
    
    def get(self, request, candidate_id, format=None):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            return Response({
                'id': candidate.id,
                'parsing_status': candidate.parsing_status,
                'parsed_at': candidate.parsed_at,
                'parsing_error': candidate.parsing_error,
            }, status=status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            return Response(
                {'error': 'Candidate not found'},
                status=status.HTTP_404_NOT_FOUND
            )
