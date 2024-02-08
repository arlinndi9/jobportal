from django import forms
from job_portal.models import JobApplication,Job

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('full_name', 'email', 'phone_number', 'cover_letter', 'resume')

class JobForm(forms.ModelForm):
    class Meta:
        model=Job
        fields="__all__"