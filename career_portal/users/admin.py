from django.contrib import admin
from .models import UserProfile, Certificate, User

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Certificate)
admin.site.register(User)