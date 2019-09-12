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