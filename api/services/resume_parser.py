"""
Resume Parser Service using Google Gemini.
Extracts structured information from resume files (PDF, DOCX).
"""
import os
import logging
import json
import re
from typing import List, Optional, Tuple
from datetime import datetime
from pathlib import Path

from django.utils import timezone
from django.conf import settings

import PyPDF2
from docx import Document

from api.schemas import (
    PersonalInfoSchema,
    EducationSchema,
    ExperienceSchema,
    SkillSchema,
    ProjectSchema,
    CertificationSchema,
    ParsedResumeSchema,
)
from api.models import (
    Candidate,
    Education,
    Experience,
    Skill,
    Project,
    Certification,
)

logger = logging.getLogger(__name__)


class ResumeParserService:
    """Service for parsing resumes using Gemini."""
    
    def __init__(self):
        """Initialize the parser with Gemini model."""
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable not set. "
                "Please add it to your .env file."
            )
        
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={
                "temperature": 0.1,
            }
        )
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from PDF or DOCX file.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Extracted text content
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = file_path.suffix.lower()
        
        try:
            if extension == '.pdf':
                return self._extract_pdf(file_path)
            elif extension in ['.docx', '.doc']:
                return self._extract_docx(file_path)
            else:
                raise ValueError(
                    f"Unsupported file format: {extension}. "
                    "Supported formats: .pdf, .docx, .doc"
                )
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise
    
    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    
    def _extract_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    def _extract_json_from_response(self, response_text: str) -> dict:
        """
        Extract JSON from model response, handling markdown code blocks.
        
        Args:
            response_text: Raw response text from the model
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        raise ValueError(f"Could not extract valid JSON from response: {response_text[:200]}...")
    
    def parse_resume(self, candidate: Candidate) -> ParsedResumeSchema:
        """
        Main orchestration method - parses entire resume in one API call.
        
        Args:
            candidate: Candidate model instance
            
        Returns:
            ParsedResumeSchema with all extracted data
        """
        try:
            candidate.parsing_status = 'processing'
            candidate.save()
            
            file_path = candidate.resume_file.path
            logger.info(f"Parsing resume from: {file_path}")
            text = self.extract_text(file_path)
            
            prompt = f"""You are a resume parser. Extract ALL information from the resume text below.

CRITICAL: Return your response as a VALID JSON object ONLY. Do not include any explanatory text, markdown formatting, or code blocks. Just the raw JSON.

JSON Schema:
{{
  "personal_info": {{
    "name": "string (required)",
    "email": "string or null",
    "phone": "string or null",
    "location": "string or null",
    "linkedin_url": "string or null",
    "github_url": "string or null",
    "summary": "string or null",
    "confidence_score": "integer 0-100 (required)"
  }},
  "education": [
    {{
      "degree": "string (required)",
      "institution": "string (required)",
      "start_date": "string or null",
      "end_date": "string or null",
      "gpa": "string or null",
      "description": "string or null",
      "confidence_score": "integer 0-100 (required)"
    }}
  ],
  "experience": [
    {{
      "company": "string (required)",
      "position": "string (required)",
      "start_date": "string or null",
      "end_date": "string or null",
      "description": "string or null",
      "skills_used": ["array of strings or null"],
      "confidence_score": "integer 0-100 (required)"
    }}
  ],
  "skills": [
    {{
      "name": "string (required)",
      "proficiency": "string or null",
      "category": "string or null",
      "confidence_score": "integer 0-100 (required)"
    }}
  ],
  "projects": [
    {{
      "name": "string (required)",
      "description": "string (required)",
      "technologies": ["array of strings or null"],
      "url": "string or null",
      "start_date": "string or null",
      "end_date": "string or null",
      "confidence_score": "integer 0-100 (required)"
    }}
  ],
  "certifications": [
    {{
      "name": "string (required)",
      "issuer": "string (required)",
      "issue_date": "string or null",
      "expiry_date": "string or null",
      "credential_id": "string or null",
      "credential_url": "string or null",
      "confidence_score": "integer 0-100 (required)"
    }}
  ]
}}

Resume text:
{text}

Response (JSON only):"""
            
            response = self.model.generate_content(prompt)
            result_json = self._extract_json_from_response(response.text)
            
            personal_info = PersonalInfoSchema(**result_json.get('personal_info', {}))
            education = [EducationSchema(**edu) for edu in result_json.get('education', [])]
            experience = [ExperienceSchema(**exp) for exp in result_json.get('experience', [])]
            skills = [SkillSchema(**skill) for skill in result_json.get('skills', [])]
            projects = [ProjectSchema(**proj) for proj in result_json.get('projects', [])]
            certifications = [CertificationSchema(**cert) for cert in result_json.get('certifications', [])]
            
            parsed_data = ParsedResumeSchema(
                personal_info=personal_info,
                education=education,
                experience=experience,
                skills=skills,
                projects=projects,
                certifications=certifications,
            )
            
            logger.info(f"Successfully parsed resume for candidate {candidate.id}")
            logger.info(f"Extracted: {len(education)} education, {len(experience)} experience, {len(skills)} skills")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            candidate.parsing_status = 'failed'
            candidate.parsing_error = str(e)
            candidate.save()
            raise
    
    def calculate_confidence_score(self, parsed_data: ParsedResumeSchema) -> float:
        """
        Calculate average confidence score from AI-provided scores.
        
        Args:
            parsed_data: Parsed resume data with confidence scores
            
        Returns:
            Average confidence score between 0.0 and 1.0
        """
        scores = []
        
        scores.append(parsed_data.personal_info.confidence_score)
        
        for edu in parsed_data.education:
            scores.append(edu.confidence_score)
        
        for exp in parsed_data.experience:
            scores.append(exp.confidence_score)
        
        for skill in parsed_data.skills:
            scores.append(skill.confidence_score)
        
        for project in parsed_data.projects:
            scores.append(project.confidence_score)
        
        for cert in parsed_data.certifications:
            scores.append(cert.confidence_score)
        
        if not scores:
            return 0.0
        
        average_score = sum(scores) / len(scores)
        return round(average_score / 100, 2)

    
    def save_to_database(
        self, 
        candidate: Candidate, 
        parsed_data: ParsedResumeSchema
    ) -> Candidate:
        """
        Save parsed data to Django models.
        
        Args:
            candidate: Candidate model instance
            parsed_data: Validated parsed resume data
            
        Returns:
            Updated Candidate instance
        """
        try:
            personal = parsed_data.personal_info
            candidate.name = personal.name
            candidate.email = personal.email or ''
            candidate.phone = personal.phone or ''
            candidate.location = personal.location or ''
            candidate.linkedin_url = personal.linkedin_url or ''
            candidate.github_url = personal.github_url or ''
            candidate.summary = personal.summary or ''
            candidate.parsed_at = timezone.now()
            candidate.parsing_status = 'completed'
            
            confidence_score = self.calculate_confidence_score(parsed_data)
            candidate.confidence_score = confidence_score
            logger.info(f"Calculated average confidence score: {confidence_score}")
            
            candidate.save()
            
            for edu in parsed_data.education:
                Education.objects.create(
                    candidate=candidate,
                    degree=edu.degree,
                    institution=edu.institution,
                    start_date=edu.start_date or '',
                    end_date=edu.end_date or '',
                    gpa=edu.gpa or '',
                    description=edu.description or '',
                )
            
            for exp in parsed_data.experience:
                Experience.objects.create(
                    candidate=candidate,
                    company=exp.company,
                    position=exp.position,
                    start_date=exp.start_date or '',
                    end_date=exp.end_date or '',
                    description=exp.description or '',
                    skills_used=exp.skills_used or [],
                )
            
            for skill in parsed_data.skills:
                Skill.objects.create(
                    candidate=candidate,
                    name=skill.name,
                    proficiency=skill.proficiency or '',
                    category=skill.category or '',
                )
            
            for project in parsed_data.projects:
                Project.objects.create(
                    candidate=candidate,
                    name=project.name,
                    description=project.description,
                    technologies=project.technologies or [],
                    url=project.url or '',
                    start_date=project.start_date or '',
                    end_date=project.end_date or '',
                )
            
            for cert in parsed_data.certifications:
                Certification.objects.create(
                    candidate=candidate,
                    name=cert.name,
                    issuer=cert.issuer,
                    issue_date=cert.issue_date or '',
                    expiry_date=cert.expiry_date or '',
                    credential_id=cert.credential_id or '',
                    credential_url=cert.credential_url or '',
                )
            
            logger.info(f"Successfully saved parsed data for candidate {candidate.id}")
            return candidate
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            candidate.parsing_status = 'failed'
            candidate.parsing_error = f"Database error: {str(e)}"
            candidate.save()
            raise
