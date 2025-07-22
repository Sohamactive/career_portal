from django.urls import path,include
from . import views

app_name = 'internships'

urlpatterns = [
    path("",views.internship_listing_view,name="internship_listing"),
    path("<int:int_id>/",views.internship_detail_view,name="internship_detail")
]
