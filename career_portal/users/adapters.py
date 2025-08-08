# sohamactive/career_portal/Sohamactive-career_portal-42f0474308d78409a65884ad136374ac6fd7042a/career_portal/users/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Intercepts the login process right after the user authenticates with
        their social provider.
        """
        # If the user is already logged in or the social account already exists,
        # let the standard login process continue.
        if request.user.is_authenticated or sociallogin.is_existing:
            return

        # For brand new signups, we stop the login process.
        # We save the social login data to the session and redirect to our DOB form.
        request.session['sociallogin_data'] = sociallogin.serialize()
        return redirect('users:social_dob')