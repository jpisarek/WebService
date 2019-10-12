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

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    search_fields = ['organization', 'name', 'level']
    fields = ('organization', 'name', 'level')
    list_display = ('organization', 'name', 'level')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'content']
    fields = ('name', 'content')
    list_display = ('name', 'content')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content', 'question', 'is_boolean']
    fields = ('content', 'question', 'is_boolean')
    list_display = ('content', 'question', 'is_boolean')