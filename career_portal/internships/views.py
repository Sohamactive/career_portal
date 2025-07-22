from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Internship
# Create your views here.
def internship_listing_view(request):
    internships = Internship.objects.filter(is_active = True).order_by('-created_at')
    context = {
        'internships' : internships
    }
    return render(request,"internships/internship_listing.html",context)

def internship_detail_view(request,int_id):
    internship = get_object_or_404(Internship,id = int_id )
    sentences = [s.strip() for s in internship.requirements.split('.') if s.strip()]
    eligibilties = [s.strip() for s in internship.eligibility.split('.') if s.strip()]
    context = {
        'internship' : internship,
        'sentences' : sentences,
        'eligibilties':eligibilties,
    }
    return render(request,"internships/internship_detail.html",context)