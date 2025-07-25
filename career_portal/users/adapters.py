from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        try:
            profile = user.profile
            if not profile.dob:
                return reverse('users:social_dob')
        except:
            return reverse('users:social_dob')

        return super().get_login_redirect_url(request)