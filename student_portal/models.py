from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    degree = models.CharField(max_length=100)
    school = models.CharField(max_length=150)
    skills = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    company_name = models.CharField(max_length=100)
    website = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
