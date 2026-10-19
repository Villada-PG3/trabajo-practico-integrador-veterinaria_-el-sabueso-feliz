from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)


handler404 = 'config.urls.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sabueso_feliz.urls')),
]
