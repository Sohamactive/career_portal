# applications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from internships.models import Internship
from .models import Application
from .forms import ApplicationForm

@login_required
def apply_view(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    profile = request.user.profile

    # --- GUARD CHECKS ---
    # 1. Check if profile is complete
    if not profile.is_profile_complete or not profile.resume:
        messages.error(request, 'Please complete your profile and upload a resume before applying.')
        return redirect('users:edit_profile')

    # 2. Check if already applied
    if Application.objects.filter(user=request.user, internship=internship).exists():
        messages.info(request, 'You have already applied for this internship.')
        return redirect('users:my_internships')

    # 3. Check if currently working
    if Application.objects.filter(user=request.user, status='working').exists():
        messages.error(request, 'You cannot apply for new internships while you are in a "working" state.')
        return redirect('internships:internship_listing')
        
    # --- FORM HANDLING ---
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = Application.objects.create(
                user=request.user,
                internship=internship,
                # --- CORRECTION 1: Changed 'cover_letter' to 'sop' ---
                sop=form.cleaned_data.get('cover_letter'),
                # --- CORRECTION 2: Changed 'resume_snapshot' to 'resume' ---
                resume=profile.resume 
            )
            application.save()
            
            messages.success(request, f'Your application for "{internship.title}" has been submitted!')
            return redirect('users:my_internships')
    else:
        form = ApplicationForm()

    context = {
        'internship': internship,
        'form': form,
        # 'messages':messages,
    }
    return render(request, 'applications/apply.html', context)
@login_required
def accepted_view(request,app_id):
    if request.method == "POST" :
        x=get_object_or_404(Application, id=app_id)
        x.status='accepted'
        x.save()
    
    return redirect('users:my_internships')
@login_required
def declined_view(request,app_id):
    x=get_object_or_404(Application, id=app_id)
    x.status='declined'
    x.save()
    return redirect('users:my_internships')

