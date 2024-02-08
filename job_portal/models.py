from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category=models.CharField(max_length=255,default='')
    requirements=models.TextField(null=True)
    bonus_skills=models.TextField(null=True)
    name_company=models.CharField(max_length=255,default='')
    about_company=models.TextField(null=True)
    location=models.TextField(null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField()

    def is_expired(self):
        return self.expiration_date < timezone.now()

    def delete_if_expired(self):
        if self.is_expired():
            self.delete()

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
