# users/auth0_backend.py

from django.contrib.auth.backends import BaseBackend
from .models import User

class Auth0Backend(BaseBackend):
    """
    Custom Django authentication backend for Auth0.
    """
    def authenticate(self, request, **kwargs):
        # This method is not used for the initial authentication,
        # as Auth0 handles that. It's here for compatibility.
        return None

    def get_user(self, user_id):
        """
        Allows Django to fetch the user object after login.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None