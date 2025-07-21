from django.shortcuts import render

# Create your views here.
def internship_listing_view(request):

    return render(request,"internships/internship_listing.html")