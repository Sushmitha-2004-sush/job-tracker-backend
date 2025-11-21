from django.contrib import admin
from .models import JobApplication, UserProfile

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'job_title', 'status', 'application_date', 'user']
    list_filter = ['status', 'application_date']
    search_fields = ['company_name', 'job_title']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile_number', 'created_at']
    search_fields = ['user__username', 'mobile_number']
