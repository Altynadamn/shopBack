from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('auth/', include('users.urls')),
]


