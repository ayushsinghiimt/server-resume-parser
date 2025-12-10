from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):
    """Main candidate model with resume file and personal information."""
    
    PARSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # File and timestamps
    resume_file = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    parsed_at = models.DateTimeField(null=True, blank=True)
    parsing_status = models.CharField(
        max_length=20, 
        choices=PARSING_STATUS_CHOICES, 
        default='pending'
    )
    parsing_error = models.TextField(null=True, blank=True)
    confidence_score = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="AI confidence score for parsing quality (0.0 to 1.0)"
    )
    
    aadhar_document = models.FileField(upload_to='documents/aadhar/', null=True, blank=True)
    pan_document = models.FileField(upload_to='documents/pan/', null=True, blank=True)
    
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
    
    def __str__(self):
        if self.name:
            return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"
        return f"Resume #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"


class Education(models.Model):
    """Education history for a candidate."""
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name='education'
    )
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    gpa = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Experience(models.Model):
    """Work experience for a candidate."""
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name='experience'
    )
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    skills_used = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'
    
    def __str__(self):
        return f"{self.position} at {self.company}"


class Skill(models.Model):
    """Skills extracted from resume."""
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Projects from resume."""
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    technologies = models.JSONField(default=list, blank=True)
    url = models.URLField(blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.name


class Certification(models.Model):
    """Certifications from resume."""
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name='certifications'
    )
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.CharField(max_length=50, blank=True)
    expiry_date = models.CharField(max_length=50, blank=True)
    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
    
    def __str__(self):
        return f"{self.name} - {self.issuer}"


