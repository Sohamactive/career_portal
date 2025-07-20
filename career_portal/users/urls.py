from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # The main signup page with choices
    path('signup/', views.signup_choice_view, name='signup_choice'),
    
    # The email-specific signup flow
    path('signup/email/', views.signup_email_view, name='signup_email'),
    path('signup/otp_verify/', views.otp_verify_view, name='otp_verify'),
    path('signup/set_password/', views.set_password_view, name='set_password'),
    
    # The flow for social logins
    path('signup/social_dob/', views.social_dob_view, name='social_dob'),
    
    # The final profile completion step
    path('profile/complete/', views.complete_profile_view, name='complete_profile'),
    
    # The login page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
