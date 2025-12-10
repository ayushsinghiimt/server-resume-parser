from django.contrib import admin
from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'resume_file', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

