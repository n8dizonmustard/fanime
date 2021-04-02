from django.shortcuts import render
import requests

# Create your views here.

def home(request):
    response = requests.get('https://kitsu.io/api/edge/anime').json()
    return render(request, 'home.html',{'response':response})

def profile(request):
    return render(request, 'profile.html')