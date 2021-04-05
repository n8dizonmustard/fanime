from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Anime, Comment, Profile
from .forms import CommentForm
import requests
import random as r
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
  page = '0'
  #making initial request to api for first of the anime list
  response = requests.get(f'https://kitsu.io/api/edge/anime?fields%5Banime%5D=slug%2CcanonicalTitle%2Ctitles%2CposterImage%2Csynopsis%2CaverageRating%2CstartDate%2CpopularityRank%2CratingRank%2CyoutubeVideoId&filter%5Bcategories%5D=action&page%5Boffset%5D=0&page%5Blimit%5D=20&sort=-user_count').json()
  return render(request, 'home.html',{'response':response, 'page':page}) #rendering home page with the contents of the response
                                                                          #from the api and the page number

def detail(request, api_anime_id):
  print(api_anime_id) #api_anime_id is the id im getting from the api not our models
  comment_form = CommentForm() 
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json() #making new request to api with anime id
  return render(request, 'detail.html', {'response': response, 'api_anime_id':api_anime_id, 'comment_form':comment_form})


##runs when user clicks a category option
def categories(request,category):
  page = 0
  response = requests.get(f'https://kitsu.io/api/edge/anime/?filter[categories]={category}').json() ##category will be diff depending on button
  return render(request, 'category.html', {'response': response, 'category':category, 'page':page})

#when a user hits next on category page than add 10 to page make new request to api and render new view
def categories_next(request,category, page):
  page = page + 10
  response = requests.get(f'https://kitsu.io/api/edge/anime?filter%5Bcategories%5D=adventure&page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'categories/next.html', {'response':response, 'category':category,'page':page})





#still not working sorry
@login_required
def add_comment(request, api_anime_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.anime_id = api_anime_id
    new_comment.save()
  return redirect('detail', api_anime_id=api_anime_id)


#this is cool. random animes when you dont know what to watch
#should we make this login users only?
def random(request):
  api_anime_id = r.randint(0,4292)
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json()
  return render(request,'detail.html', {'response':response,'api_anime_id':api_anime_id})

#Showing most popular animes according to kitsu
#I think we should change our layout and put this on homepage?
def library(request):
  page = 0
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'library.html', {'response':response,'page':page})
  
def next(request, page):
  page = page + 5 # if a user hit the next button then whatever page is currently at +5 to get the new response
  print(page) # this will help you if you wanna see it in terminal. Helped me
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'next.html', {'response':response, 'page': page})

def previous(request, page):
  page = page - 5 #same as next but backward
  print(page)
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'previous.html', {'response':response, 'page': page})

def first(request):
  page = '0' #if user hits first page page = 0 
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'library.html',{'response':response, 'page':page})

def last(request):
  page = '16143' # according to api docs 16543 is the last page number
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=10&page%5Boffset%5D={page}').json()
  return render(request, 'library.html',{'response':response, 'page':page})

@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

#if the user is logged in a edit profile form is visible. Its working but with minor problems -_- 
# you can keep clicking edit profile and it just makes a new profile every time instead of editing what you already have
class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['name', 'favorite_anime_ever', 'about' ]
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  fields = ['name', 'favorite_anime_ever', 'about']

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