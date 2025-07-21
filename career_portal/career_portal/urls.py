from django.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('account/', include('users.urls')),
    path('internship/', include('internships.urls')),
    path('applications/', include('applications.urls')),
    # Add this line for allauth
    path('accounts/', include('allauth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)