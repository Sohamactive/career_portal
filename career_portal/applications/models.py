from django.db import models
from django.conf import settings
from django.utils import timezone
from internships.models import Internship
from datetime import timedelta

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('working', 'Working'),
        ('rejected', 'Rejected'),
        ('offer_expired', 'Offer Expired'),
        ('auto_rejected', 'Auto Rejected'),
        ('declined','Declined')
    )
                            ##here we are using auth_user_model from settings to refer to the user model
                            ##instead of directly importing the User model
                            ## This allows for more flexibility, especially if a custom user model is used.
                            ## for example, if you have a custom user model, you can still use it without changing this code.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    
    sop = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')

    offer_made_at = models.DateTimeField(null=True, blank=True)
    offer_expiration = models.DurationField(default=timedelta(hours=72))  # 72-hour window

    admin_notes = models.TextField(blank=True,null=True)
    ##this meta class is used to define additional properties for the model
    ##unique_together ensures that a user can only apply once for a specific internship
    ##ordering specifies the default ordering of the objects returned by the model
    ##it orders the applications by applied_at in descending order
    class Meta:
        unique_together = ('user', 'internship')
        ordering = ['-applied_at'] 

    def is_offer_expired(self):
        if self.status == 'offered' and self.offer_made_at:
            return timezone.now() > self.offer_made_at + self.offer_expiration
        return False

    def __str__(self):
        return f"{self.user.email} → {self.internship.title} ({self.status})"

