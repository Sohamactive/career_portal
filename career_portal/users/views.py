from django.shortcuts import render,redirect
from .forms import SignUpEmailForm , OtpForm , SetPasswordForm , UserProfileForm,CertificateForm
import random
from datetime import datetime , timedelta
from django.conf import settings
from .models import User,UserProfile,Certificate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , authenticate,logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from applications.models import Application
from datetime import date
User = get_user_model()
# Create your views here.
def signup_choice_view(request):
    return render(request, 'users/signup_choice.html')

def signup_email_view(request):
    if request.method == "POST":
        form = SignUpEmailForm(request.POST)
        if form.is_valid():
            request.session['signup_email']=form.cleaned_data['email']
            request.session['signup_dob']=form.cleaned_data['dob'].isoformat()
            return redirect('users:otp_verify')
    else : 
        form = SignUpEmailForm()
    return render(request, 'users/signup_email.html',{'form':form})

def otp_verify_view(request):
    if 'signup_email' not in request.session:
        return redirect('users:signup_choice')

    # --- Already verified ---
    if request.session.get('otp_verified'):
        return redirect('users:set_password')

    if request.method == "POST":
        otp_entered = "".join(request.POST.get(f'otp_{i}','') for i in range(1,7))
        form = OtpForm({'otp': otp_entered})

        if form.is_valid():
            stored_otp = request.session.get('otp')
            otp_expiry = datetime.fromisoformat(request.session.get('otp_expiry'))

            if otp_entered == stored_otp and datetime.now() < otp_expiry:
                del request.session['otp']
                del request.session['otp_expiry']
                request.session['otp_verified'] = True  # ✅ Set this!
                return redirect("users:set_password")

            error = "Invalid or expired OTP. Please try again."
            return render(request, 'users/otp_verify.html', {'error': error})

    else:
        otp_expiry_str = request.session.get('otp_expiry')
        should_generate_new_otp = True

        if otp_expiry_str:
            otp_expiry = datetime.fromisoformat(otp_expiry_str)
            if datetime.now() < otp_expiry:
                should_generate_new_otp = False

        if should_generate_new_otp:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=10)).isoformat()
            print(f"NEW OTP for {request.session['signup_email']}: {otp}")

    return render(request, 'users/otp_verify.html')

def set_password_view(request):
    # Check if user has completed the previous steps
    if not request.session.get('otp_verified'):
        return redirect('users:otp_verify')

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            # Retrieve the user's data from the session
            email = request.session.get('signup_email')
            dob_str = request.session.get('signup_dob')
            password = form.cleaned_data['password']

            if not email or not dob_str:
                # If session data is missing, send them back to the start
                return redirect('users:signup_choice')
            
            # --- This is where we create the user! ---
            user = User.objects.create_user(email=email, password=password)
            
            # Create the associated UserProfile
            UserProfile.objects.create(
                user=user,
                dob=datetime.fromisoformat(dob_str).date()
            )
            user.backend = settings.AUTHENTICATION_BACKENDS[0] 
            # Log the new user in automatically
            login(request, user)

            # Clean up the session data
            

            # Redirect to the final step
            return redirect('users:complete_profile')
    else:
        form = SetPasswordForm()

    return render(request, 'users/set_password.html', {'form': form})

def social_dob_view(request):
    return render(request, 'users/social_dob.html')

def complete_profile_view(request):
    # Redirect if user is not logged in
    if not request.user.is_authenticated:
        return redirect('users:login')

    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # This case should ideally not happen if our signup flow is correct
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        # We pass 'instance=profile' to update the existing profile
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            # Save the main profile form
            profile = form.save(commit=False)
            profile.is_profile_complete = True # Mark the profile as complete
            profile.save()

            # --- Handle Certificate Uploads ---
            # Clear existing certificates to avoid duplicates on re-submission
            profile.certificates.all().delete()
            
            # The 'request.POST.getlist' method gets all values for a given key
            certificate_titles = request.POST.getlist('cert_title')
            certificate_files = request.FILES.getlist('cert_file')
            
            for i in range(len(certificate_titles)):
                if certificate_titles[i] and certificate_files[i]:
                    Certificate.objects.create(
                        user_profile=profile,
                        title=certificate_titles[i],
                        file=certificate_files[i]
                    )
            
            # For now, let's redirect to the homepage after completion
            return redirect('core:home')
    else:
        # On a GET request, show the form pre-filled with existing data
        form = UserProfileForm(instance=profile)

    return render(request, 'users/complete_profile.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method =="POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()

            login(request,user)

            return redirect('core:home')
    else:
        form = AuthenticationForm()


    return render(request, 'users/login.html',{'form':form})

def logout_view(request):

    logout(request)
    return render(request,"core/index.html")

@login_required
def dashboard_view(request):
    user_profile,_=UserProfile.objects.get_or_create(user = request.user)
    certificates = user_profile.certificates.all()
    age = None
    if user_profile.dob:
        today = date.today()
        age = today.year - user_profile.dob.year - (
            (today.month, today.day) < (user_profile.dob.month, user_profile.dob.day)
        )
    context={
        'user_profile': user_profile,
        'user': request.user,
        'certificates':certificates,
        'age':age
    }
    return render(request, 'users/dashboard.html',context)

def edit_profile_view(request):
    profile= request.user.profile
    next_url=request.GET.get('next') or request.POST.get('next') or 'users:dashboard'
    if request.method == "POST" : 
        form = UserProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
            form.save()
            certs_to_delete_ids = request.POST.getlist('delete_cert')
            if certs_to_delete_ids:
                Certificate.objects.filter(id__in = certs_to_delete_ids,user_profile=profile).delete()
            new_cert_titles = request.POST.getlist('new_cert_title')
            new_cert_files = request.FILES.getlist('new_cert_file')
            for i in range(len(new_cert_titles)):
                if new_cert_titles[i] and new_cert_files[i]:
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
        'certificates':profile.certificates.all()
    }
    
    return render(request,"users/edit_profile.html",context)

def my_internships_view(request):
    applications = Application.objects.filter(user=request.user)
    context = {
        'applications' : applications
    }
    return render(request,"users/my_internships.html",context)