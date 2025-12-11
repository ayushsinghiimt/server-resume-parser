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
    CandidateListSerializer,
    DocumentUploadSerializer,
)
from .services.resume_parser import ResumeParserService

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """Lightweight health check endpoint for serverless cold start detection."""
    
    def get(self, request):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class DocumentUploadView(APIView):
    """Upload identity documents for a candidate."""
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, candidate_id, format=None):
        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response(
                {'error': 'Candidate not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DocumentUploadSerializer(
            candidate,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            detail_serializer = CandidateDetailSerializer(candidate, context={'request': request})
            return Response(detail_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentRequestView(APIView):
    """Generate AI-powered personalized document request email."""
    
    def post(self, request, candidate_id, format=None):
        import google.generativeai as genai
        import os
        import json
        
        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response(
                {'error': 'Candidate not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""Generate a professional and personalized email requesting government ID documents from a job candidate.

Candidate Information:
Name: {candidate.name or 'Candidate'}
Email: {candidate.email or 'N/A'}
Position Applied: {candidate.experience.first().position if candidate.experience.exists() else 'N/A'}

CRITICAL: Return ONLY a valid JSON object with exactly this structure:
{{
  "subject": "string - email subject line",
  "body": "string - full email body with proper formatting, use \\n for line breaks"
}}

The email should:
- Be warm and professional
- Explain that we need Aadhar and PAN documents for verification
- Mention it's a standard part of the hiring process
- Provide clear instructions
- Be personalized with the candidate's name
- End with a professional signature from "HR Team"

Response (JSON only):"""
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                response_text = response_text[json_start:json_end].strip()
            elif '```' in response_text:
                json_start = response_text.find('```') + 3
                json_end = response_text.find('```', json_start)
                response_text = response_text[json_start:json_end].strip()
            
            email_data = json.loads(response_text)
            
            # Format the message for storage
            message = f"Subject: {email_data['subject']}\n\n{email_data['body']}"
            
            candidate.document_request_message = message
            candidate.save()
            
            logger.info(f"Generated document request for candidate {candidate.id}")
            
            return Response({
                'success': True,
                'message': 'Document request generated successfully',
                'email': email_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error generating document request: {e}")
            return Response(
                {'error': f'Failed to generate request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class CandidateListView(APIView):
    """List all candidates with minimal fields."""
    
    def get(self, request, format=None):
        candidates = Candidate.objects.all()
        serializer = CandidateListSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



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
