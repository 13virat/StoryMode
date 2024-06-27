from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('<int:pk>/', views.story_detail, name='story_detail'),
    path('new/', views.story_create, name='story_create'),
    path('<int:pk>/edit/', views.story_edit, name='story_edit'),
    path('accounts/signup/', views.signup, name='signup'),  # Example URL for signup
    path('accounts/login/', views.login, name='login'),
]