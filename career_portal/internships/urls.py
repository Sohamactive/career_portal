from django.urls import path,include
from . import views

app_name = 'internships'

urlpatterns = [
    path("listing/",views.internship_listing_view,name="internship_listing"),
]
