# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # --- SIGNUP FLOW ---
    path('signup/', views.signup_choice_view, name='signup_choice'),
    # Email Signup URLs
    path('signup/email/', views.signup_email_view, name='signup_email'),
    path('signup/otp_verify/', views.otp_verify_view, name='otp_verify'),
    path('signup/set_password/', views.set_password_view, name='set_password'),

    # --- LOGIN FLOW ---
    # Standard Django login for email/password
    path('login/', views.login_view, name='login'),
    # Auth0 login for social providers (Google/GitHub)
    path('social-login/', views.social_login_view, name='social_login'),
    
    # --- AUTH0 CALLBACK & LOGOUT ---
    path('callback/', views.callback_view, name='callback'),
    path('logout/', views.logout_view, name='logout'),

    # --- USER ACCOUNT FLOW ---
    path('profile/complete/', views.complete_profile_view, name='complete_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('my-internships/', views.my_internships_view, name='my_internships'),
]
