from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('stories/', include('stories.urls')),
    path('comments/', include('comments.urls')),
    path('', include('stories.urls')),  # Redirect to stories as homepage
]