from django.contrib import admin
from .models import *

admin.site.site_header = "Panel administratora"
admin.site.index_title= "Zarządzaj bazą danych"

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    search_fields = ['user', 'first_name', 'last_name', 'email', 'organization']
    fields = ('user', 'first_name', 'last_name', 'email', 'organization')
    list_display = ('user', 'first_name', 'last_name', 'email', 'organization')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['user', 'first_name', 'last_name']
    fields = ('user', 'first_name', 'last_name')
    list_display = ('user', 'first_name', 'last_name')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    search_fields = ['job_position', 'description', 'organization']
    fields = ('job_position', 'description', 'organization')
    list_display = ('job_position', 'description', 'organization')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    search_fields = ['organization', 'name', 'job_position']
    fields = ('organization', 'name', 'job_position')
    list_display = ('organization', 'name', 'job_position')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['quiz', 'content']
    fields = ('quiz', 'content')
    list_display = ('quiz', 'content')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content', 'question', 'is_true']
    fields = ('content', 'question', 'is_true')
    list_display = ('content', 'question', 'is_true')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ['candidate', 'quiz','score',  'grade','status']
    fields = ('candidate', 'quiz','score', 'grade', 'status')
    list_display = ('candidate', 'quiz','score', 'grade', 'status')