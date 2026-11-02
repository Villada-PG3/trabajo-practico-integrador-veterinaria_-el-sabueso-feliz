from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


def custom_404(request, exception):
    return render(request, '404.html', status=404)


handler404 = 'config.urls.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Clase 16: Autenticación completa
    path('', include('sabueso_feliz.urls')),
]

# Clase 8: Servir archivos media y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
