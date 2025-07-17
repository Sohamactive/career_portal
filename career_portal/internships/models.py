from django.db import models
from django.utils import timezone
# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Internship(models.Model):
    TYPE_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    skills_required = models.ManyToManyField(Skill, blank=True)
    requirements = models.TextField()
    eligibility = models.TextField()
    duration = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    application_deadline = models.DateField()

    max_positions = models.PositiveIntegerField(default=1)
    current_accepted = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def has_vacancy(self):
        return self.current_accepted < self.max_positions
    
    def is_open(self):
        return self.is_active and self.application_deadline >= timezone.now().date()
    
    def save(self, *args, **kwargs):
        if self.application_deadline < timezone.now().date():
            self.is_active = False
        super().save(*args, **kwargs)