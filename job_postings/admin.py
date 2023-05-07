from django.contrib import admin
from .models import JobPosting


# Register your models here.
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'salary', 'application_deadline')
    list_filter = ('location', 'salary')
    search_fields = ('title', 'description', 'company_name')


admin.site.register(JobPosting, JobPostingAdmin)
