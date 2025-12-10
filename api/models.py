from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):
    resume_file = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
    
    def __str__(self):
        return f"Resume #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

