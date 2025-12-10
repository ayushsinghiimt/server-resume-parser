from rest_framework import serializers
from .models import (
    Candidate,
    Education,
    Experience,
    Skill,
    Project,
    Certification,
)


class CandidateListSerializer(serializers.ModelSerializer):
    """Serializer for listing candidates with minimal fields."""
    company = serializers.SerializerMethodField()
    
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'company', 'parsing_status']
    
    def get_company(self, obj):
        latest_experience = obj.experience.first()
        return latest_experience.company if latest_experience else None



class CandidateUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading resumes."""
    class Meta:
        model = Candidate
        fields = ['id', 'resume_file', 'created_at']
        read_only_fields = ['id', 'created_at']


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for education entries."""
    class Meta:
        model = Education
        fields = [
            'id', 'degree', 'institution', 'start_date', 
            'end_date', 'gpa', 'description'
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for work experience entries."""
    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'position', 'start_date', 
            'end_date', 'description', 'skills_used'
        ]


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills."""
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'category']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects."""
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'technologies', 
            'url', 'start_date', 'end_date'
        ]


class CertificationSerializer(serializers.ModelSerializer):
    """Serializer for certifications."""
    class Meta:
        model = Certification
        fields = [
            'id', 'name', 'issuer', 'issue_date', 
            'expiry_date', 'credential_id', 'credential_url'
        ]


class CandidateDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for candidate with all related data."""
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Candidate
        fields = [
            'id', 'resume_file', 'created_at', 'parsed_at',
            'parsing_status', 'parsing_error',
            'name', 'email', 'phone', 'location',
            'linkedin_url', 'github_url', 'summary',
            'education', 'experience', 'skills', 
            'projects', 'certifications'
        ]
        read_only_fields = [
            'id', 'created_at', 'parsed_at', 'parsing_status', 
            'parsing_error'
        ]


