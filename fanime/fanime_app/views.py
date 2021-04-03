from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import requests

# Create your views here.

def home(request):
  page = '0'
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'home.html',{'response':response, 'page':page})
def detail(request, i_id):
  print(i_id)
  response = requests.get(f'https://kitsu.io/api/edge/anime/{i_id}').json()
  return render(request, 'detail.html', {'response': response})
def next(request, page):
  page = page + 5
  print(page)
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'next.html', {'response':response, 'page': page})

def previous(request, page):
  page = page - 5
  print(page)
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'previous.html', {'response':response, 'page': page})

def first(request):
  page = '0'
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'home.html',{'response':response, 'page':page})

def last(request):
  page = '16143'
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'home.html',{'response':response, 'page':page})

def profile(request):
    return render(request, 'profile.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('profile')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)