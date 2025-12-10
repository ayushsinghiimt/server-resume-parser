from django.contrib import admin
from .models import (
    Candidate,
    Education,
    Experience,
    Skill,
    Project,
    Certification,
)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'parsing_status', 'created_at']
    list_filter = ['parsing_status', 'created_at']
    readonly_fields = ['created_at', 'parsed_at']
    search_fields = ['name', 'email', 'phone']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'degree', 'institution', 'start_date', 'end_date']
    list_filter = ['institution']
    search_fields = ['degree', 'institution']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'position', 'company', 'start_date', 'end_date']
    list_filter = ['company']
    search_fields = ['position', 'company']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'name', 'category', 'proficiency']
    list_filter = ['category', 'proficiency']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'name', 'start_date', 'end_date']
    search_fields = ['name', 'description']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'name', 'issuer', 'issue_date']
    list_filter = ['issuer']
    search_fields = ['name', 'issuer']


