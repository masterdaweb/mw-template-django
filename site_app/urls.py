from django.contrib import admin
from django.urls import path

from uploads import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('health/', views.health, name='health'),
    path('status.json', views.status, name='status'),
    path('admin/', admin.site.urls),
]
