from django.shortcuts import render
from .models import UserProfile

def profile(request):
    return render(request, 'users/profile.html')
