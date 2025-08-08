from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('account/', include('users.urls')),
    path('internships/', include('internships.urls')),
    path('applications/', include('applications.urls')),
    
    # REMOVED: The line including 'allauth.urls' has been deleted
    # path('accounts/', include('allauth.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
