from django.contrib import admin

from jobs.models import JobPosting

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'created')
    list_filter = ('position', 'company', 'created')
    search_fields = ('position',)


admin.site.register(JobPosting, JobPostingAdmin)