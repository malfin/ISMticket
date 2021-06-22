from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ticketsystem import settings

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),
    path('accounts/', include('authapp.urls', namespace='authapp')),
    path('panel/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
