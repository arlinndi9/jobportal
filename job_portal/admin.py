from django.contrib import admin
from job_portal.models import Job,JobApplication
from django.utils.html import format_html


# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'name_company', 'location', 'created_at')
    list_filter = ('created_at', 'location')
    search_fields = ('title', 'name_company')

admin.site.register(Job, JobAdmin)

admin.site.register(JobApplication)



