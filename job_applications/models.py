from django.db import models
from student_portal.models import Profile
from job_postings.models import JobPosting


# Create your models here.
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Selected', 'Selected'),
        ('Not Selected', 'Not Selected'),
    ]

    student_username = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_id = models.ForeignKey(JobPosting, on_delete=models.CASCADE, to_field="job_id")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_applied = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_username.user.username} applied for job {self.job_id}"
