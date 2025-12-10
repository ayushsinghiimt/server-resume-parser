"""
Pydantic schemas for resume parsing validation.
These schemas are used by LangChain for structured output and validation.
"""
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class PersonalInfoSchema(BaseModel):
    """Personal information extracted from resume."""
    name: str = Field(description="Full name of the candidate")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City, State or full address")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    summary: Optional[str] = Field(None, description="Professional summary or objective")


class EducationSchema(BaseModel):
    """Education details from resume."""
    degree: str = Field(description="Degree name (e.g., Bachelor of Science in Computer Science)")
    institution: str = Field(description="University or college name")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY) or 'Present'")
    gpa: Optional[str] = Field(None, description="GPA or grade")
    description: Optional[str] = Field(None, description="Relevant coursework, achievements, etc.")


class ExperienceSchema(BaseModel):
    """Work experience details from resume."""
    company: str = Field(description="Company name")
    position: str = Field(description="Job title/position")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY) or 'Present'")
    description: Optional[str] = Field(None, description="Job responsibilities and achievements")
    skills_used: Optional[List[str]] = Field(None, description="Technologies and skills used in this role")


class SkillSchema(BaseModel):
    """Skill extracted from resume."""
    name: str = Field(description="Skill or technology name")
    proficiency: Optional[str] = Field(None, description="Proficiency level: Beginner, Intermediate, Advanced, Expert")
    category: Optional[str] = Field(None, description="Skill category: Programming, Framework, Tool, Soft Skill, etc.")


class ProjectSchema(BaseModel):
    """Project details from resume."""
    name: str = Field(description="Project name")
    description: str = Field(description="Project description and your role")
    technologies: Optional[List[str]] = Field(None, description="Technologies and tools used")
    url: Optional[str] = Field(None, description="Project URL or repository link")
    start_date: Optional[str] = Field(None, description="Project start date")
    end_date: Optional[str] = Field(None, description="Project end date or 'Present'")


class CertificationSchema(BaseModel):
    """Certification details from resume."""
    name: str = Field(description="Certification name")
    issuer: str = Field(description="Issuing organization")
    issue_date: Optional[str] = Field(None, description="Date when certification was issued")
    expiry_date: Optional[str] = Field(None, description="Expiry date if applicable")
    credential_id: Optional[str] = Field(None, description="Credential ID or certificate number")
    credential_url: Optional[str] = Field(None, description="URL to verify the credential")


class ParsedResumeSchema(BaseModel):
    """Complete parsed resume data."""
    personal_info: PersonalInfoSchema
    education: List[EducationSchema] = Field(default_factory=list)
    experience: List[ExperienceSchema] = Field(default_factory=list)
    skills: List[SkillSchema] = Field(default_factory=list)
    projects: List[ProjectSchema] = Field(default_factory=list)
    certifications: List[CertificationSchema] = Field(default_factory=list)
