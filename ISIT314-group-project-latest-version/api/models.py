# ================= models.py =================
from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    experience = models.IntegerField()
    skills = models.JSONField()
    # Allowed work modes for matching jobs
    WORK_MODE_CHOICES = [
        ('Remote', 'Remote'),
        ('On-site', 'On-site'), 
        ('Hybrid', 'Hybrid'),
    ]
    preferred_working_mode = models.CharField(
        max_length=10,
        choices=WORK_MODE_CHOICES
    )
    preferred_location = models.CharField(max_length=100)
    #Membership?
    is_member = models.BooleanField(default=False)

#NEEDS TO BE OBJECT ORIENTED

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    education = models.CharField(max_length=100)
    skills = models.JSONField()
    experience = models.IntegerField()
    mode = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

#NEEDS TO BE OBJECT ORIENTED
