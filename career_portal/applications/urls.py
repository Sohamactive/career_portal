from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path("apply/<int:internship_id>/",views.apply_view,name="apply"),
    path("accepted/<int:app_id>/",views.accepted_view,name="accepted"),
    path("declined/<int:app_id>/",views.declined_view,name="declined"),
]
