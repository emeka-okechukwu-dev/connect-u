from django.contrib import admin
from .models import JobApplication


# Register your models here.
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_username', 'job_id', 'status', 'date_applied')
    list_filter = ('date_applied',)
    search_fields = ('student_username__user__username', 'job_id__title', 'job_id__employer__user__username')


admin.site.register(JobApplication, JobApplicationAdmin)
