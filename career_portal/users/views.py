# users/views.py

# --- Django and Python Imports ---
import random
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode, quote_plus

# --- Third-Party Imports ---
from authlib.integrations.django_client import OAuth

# --- Local Application Imports ---
from .forms import UserProfileForm, SignUpEmailForm, OtpForm, SetPasswordForm
from .models import User, UserProfile, Certificate
from applications.models import Application

# ==============================================================================
#   Auth0 CONFIGURATION (For Social Logins)
# ==============================================================================

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

# ==============================================================================
#   AUTHENTICATION VIEWS (Hybrid: Auth0 for Social, Django for Email)
# ==============================================================================

def social_login_view(request):
    """
    Redirects the user to Auth0 for Google/GitHub authentication.
    """
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("users:callback"))
    )

def callback_view(request):
    """
    Handles the user's return from Auth0 after a social login.
    """
    token = oauth.auth0.authorize_access_token(request)
    userinfo = token.get("userinfo")
    namespace = 'https://careerportal.example.com/'
    is_new_user_claim = f'{namespace}is_new'

    if userinfo:
        email = userinfo.get("email")
        user, created = User.objects.get_or_create(email=email)

        if created:
            UserProfile.objects.create(user=user)
        
        auth_login(request, user, backend='users.auth0_backend.Auth0Backend')
        
        if userinfo.get(is_new_user_claim):
            return redirect('users:complete_profile')
        else:
            return redirect('users:dashboard')

    return redirect('core:home')

def logout_view(request):
    """
    Logs the user out from both Django and Auth0 sessions.
    """
    auth_logout(request)
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {"returnTo": request.build_absolute_uri(reverse("core:home")), "client_id": settings.AUTH0_CLIENT_ID},
            quote_via=quote_plus,
        ),
    )

def login_view(request):
    """
    Handles the standard Django email/password login form.
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('users:dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

# ==============================================================================
#   EMAIL SIGNUP FLOW (Restored from your original code)
# ==============================================================================

def signup_choice_view(request):
    return render(request, 'users/signup_choice.html')

def signup_email_view(request):
    if request.method == "POST":
        form = SignUpEmailForm(request.POST)
        if form.is_valid():
            request.session['signup_email'] = form.cleaned_data['email']
            request.session['signup_dob'] = form.cleaned_data['dob'].isoformat()
            return redirect('users:otp_verify')
    else:
        form = SignUpEmailForm()
    return render(request, 'users/signup_email.html', {'form': form})

def otp_verify_view(request):
    if 'signup_email' not in request.session:
        return redirect('users:signup_choice')

    if request.session.get('otp_verified'):
        return redirect('users:set_password')

    if request.method == "POST":
        otp_entered = "".join(request.POST.get(f'otp_{i}', '') for i in range(1, 7))
        stored_otp = request.session.get('otp')
        otp_expiry = datetime.fromisoformat(request.session.get('otp_expiry'))

        if otp_entered == stored_otp and datetime.now() < otp_expiry:
            request.session['otp_verified'] = True
            return redirect("users:set_password")
        else:
            error = "Invalid or expired OTP. Please try again."
            return render(request, 'users/otp_verify.html', {'error': error})
    else:
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp
        request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=10)).isoformat()
        print(f"OTP for {request.session['signup_email']}: {otp}") # Replace with actual email sending
        return render(request, 'users/otp_verify.html')

def set_password_view(request):
    if not request.session.get('otp_verified'):
        return redirect('users:otp_verify')

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            email = request.session.get('signup_email')
            dob_str = request.session.get('signup_dob')
            password = form.cleaned_data['password']

            if not email or not dob_str:
                return redirect('users:signup_choice')
            
            user = User.objects.create_user(email=email, password=password)
            UserProfile.objects.create(user=user, dob=datetime.fromisoformat(dob_str).date())
            
            # Clean up session
            for key in ['signup_email', 'signup_dob', 'otp', 'otp_expiry', 'otp_verified']:
                if key in request.session:
                    del request.session[key]
            
            auth_login(request, user)
            return redirect('users:complete_profile')
    else:
        form = SetPasswordForm()

    return render(request, 'users/set_password.html', {'form': form})

# ==============================================================================
#   USER JOURNEY VIEWS (Shared by both flows)
# ==============================================================================

@login_required
def complete_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_profile_complete = True
            profile.save()
            profile.certificates.all().delete()
            certificate_titles = request.POST.getlist('cert_title')
            certificate_files = request.FILES.getlist('cert_file')
            for i in range(len(certificate_titles)):
                if certificate_titles[i] and len(certificate_files) > i:
                    Certificate.objects.create(
                        user_profile=profile,
                        title=certificate_titles[i],
                        file=certificate_files[i]
                    )
            return redirect('users:dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/complete_profile.html', {'form': form})

@login_required
def dashboard_view(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    certificates = user_profile.certificates.all()
    age = None
    if user_profile.dob:
        today = date.today()
        age = today.year - user_profile.dob.year - ((today.month, today.day) < (user_profile.dob.month, user_profile.dob.day))
    context = {
        'user_profile': user_profile,
        'user': request.user,
        'certificates': certificates,
        'age': age
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    next_url = request.GET.get('next') or request.POST.get('next') or 'users:dashboard'
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            certs_to_delete_ids = request.POST.getlist('delete_cert')
            if certs_to_delete_ids:
                Certificate.objects.filter(id__in=certs_to_delete_ids, user_profile=profile).delete()
            new_cert_titles = request.POST.getlist('new_cert_title')
            new_cert_files = request.FILES.getlist('new_cert_file')
            for i in range(len(new_cert_titles)):
                if new_cert_titles[i] and len(new_cert_files) > i:
                    Certificate.objects.create(
                        user_profile=profile,
                        title=new_cert_titles[i],
                        file=new_cert_files[i]
                    )
            return redirect(next_url)
    else:
        form = UserProfileForm(instance=profile)
    context = {
        'form': form,
        'certificates': profile.certificates.all()
    }
    return render(request, "users/edit_profile.html", context)

@login_required
def my_internships_view(request):
    applications = Application.objects.filter(user=request.user)
    context = {'applications': applications}
    return render(request, "users/my_internships.html", context)
