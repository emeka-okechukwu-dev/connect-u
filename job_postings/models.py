from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'),
                        ('Temporary', 'Temporary'), ('Volunteer', 'Volunteer'), ('Internship', 'Internship'),
                        ('Other', 'Other')]

    JOB_CATEGORY_CHOICES = {('Education', 'Education'), ('Business', 'Business'), ('Healthcare', 'Healthcare'),
                            ('Technology', 'Technology'), ('Arts and entertainment', 'Arts and entertainment'),
                            ('Other', 'Other')}

    job_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    company_name = models.CharField(max_length=255)
    website = models.CharField(max_length=200)
    job_type = models.CharField(max_length=255, choices=JOB_TYPE_CHOICES)
    job_category = models.CharField(max_length=255, choices=JOB_CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    application_deadline = models.DateField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return f"Job ID: {self.job_id}"
