from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from . import views 

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('follow/', views.follow, name='follow'),
    path('<str:username>/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)