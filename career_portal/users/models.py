from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# --- Custom User Model Setup ---

# This is the manager for our new User model. It tells Django how to create
# regular users and superusers.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# This is our new, primary User model.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False) # Required for admin access
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # This sets the email field as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # No other fields are required for createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# --- Your Profile and Certificate Models ---

# These upload functions are great! Let's adapt them slightly.
def upload_to_cert(instance, filename):
    return f'certificates/user_{instance.user_profile.user.id}/{filename}'

def upload_to_resume(instance, filename):
    return f'resumes/user_{instance.user.id}/{filename}'

def upload_to_profile_pic(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    # This now correctly links to our custom User model above
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=upload_to_profile_pic, blank=True, null=True)
    resume = models.FileField(upload_to=upload_to_resume, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # We'll use this flag to manage the onboarding flow
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email # We can now use email directly

class Certificate(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to=upload_to_cert)
    title = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Certificate'} - {self.user_profile.user.email}"