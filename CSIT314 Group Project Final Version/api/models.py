# ================= models.py =================
from django.db import models


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('candidate', 'Candidate'),
        ('business', 'Business'),
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES
    )

    def __str__(self):
        return self.email

class Candidate(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

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

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

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

    business = models.ForeignKey(
        'Business',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    education = models.CharField(max_length=100)
    skills = models.JSONField()
    experience = models.IntegerField()
    salary = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Business(models.Model):
    account = models.OneToOneField(
    Account,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    business_name = models.CharField(max_length=100)
    abn = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    description = models.TextField()
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name
    

class SavedJob(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate.name} saved {self.job.title}"
    

class Match(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Shortlisted', 'Shortlisted'),
        ('Contacted', 'Contacted'),
        ('Rejected', 'Rejected'),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='New'
    )

    class Meta:
        unique_together = ('business', 'candidate')

    def __str__(self):
        return f"{self.business.business_name} matched with {self.candidate.name}"