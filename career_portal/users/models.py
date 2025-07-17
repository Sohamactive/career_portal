from django.db import models
from django.conf import settings

def upload_to_cert(instance, filename):
    return f'certificates/user_{instance.user_profile.user.id}/{filename}'

def upload_to_resume(instance, filename):
    return f'resumes/user_{instance.user.id}/{filename}'

def upload_to_profile_pic(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField()
    profile_picture = models.ImageField(upload_to=upload_to_profile_pic, blank=True, null=True)
    resume = models.FileField(upload_to=upload_to_resume, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField()
    github_url = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    max_position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.id} : {self.user.username}'

class Certificate(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to=upload_to_cert)
    title = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Certificate'} - {self.user_profile.user.id}: {self.user_profile.user.username}"
