from django.shortcuts import render
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.
def apply_view(request):
    return render(request,"applications/apply.html")