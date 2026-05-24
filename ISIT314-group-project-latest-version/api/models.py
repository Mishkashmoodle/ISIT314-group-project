# ================= models.py =================
from django.db import models


class Candidate(models.Model):

# choice of being a candidate or a company, default is candidate
    USER_TYPE_CHOICES = [
        ('Candidate', 'Candidate'),
        ('Company', 'Company'),
    ]

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='Candidate'
    )

    education = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    experience = models.IntegerField()
    skills = models.JSONField()

    # allowed workk mode for matching jobs
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

    # membership status 
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    education = models.CharField(max_length=100)
    skills = models.JSONField()
    experience = models.IntegerField()
    mode = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.title
