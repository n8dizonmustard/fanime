from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Anime, Comment, Profile, Photo
from .forms import CommentForm
import requests
import random as r
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3   

S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'
BUCKET = 'simanutui'


def home(request):
  page = '0'
  #making initial request to api for first of the anime list
  response = requests.get(f'https://kitsu.io/api/edge/anime?fields%5Banime%5D=slug%2CcanonicalTitle%2Ctitles%2CposterImage%2Csynopsis%2CaverageRating%2CstartDate%2CpopularityRank%2CratingRank%2CyoutubeVideoId&filter%5Bcategories%5D=action&page%5Boffset%5D=0&page%5Blimit%5D=18&sort=-user_count').json()
  return render(request, 'home.html',{'response':response, 'page':page}) #rendering home page with the contents of the response
                                                                          #from the api and the page number

def detail(request, api_anime_id, api_anime_name):
  comment_form = CommentForm() 
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json()
  comments = Comment.objects.filter(anime_id = api_anime_id)
  api_anime_img = response['data']['attributes']['posterImage']['small']
  new_anime = Anime(api_anime_id, api_anime_id, api_anime_name, api_anime_img)
  new_anime.save()
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json() #making new request to api with anime id
  return render(request, 'detail.html', {'response': response, 'api_anime_id':api_anime_id, 'comment_form':comment_form, 'comments':comments})

def forum(request):
  return render(request, 'forum.html')
##runs when user clicks a category option
def categories(request,category):
  page = 0
  response = requests.get(f'https://kitsu.io/api/edge/anime?filter%5Bcategories%5D={category}&page%5Blimit%5D=9&page%5Boffset%5D={page}').json() ##category will be diff depending on button
  return render(request, 'category.html', {'response': response, 'category':category, 'page':page})

#when a user hits next on category page than add 10 to page make new request to api and render new view
def categories_next(request,category, page):
  page = page + 10
  response = requests.get(f'https://kitsu.io/api/edge/anime?filter%5Bcategories%5D={category}&page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'categories/next.html', {'response':response, 'category':category,'page':page})

def categories_previous(request,category, page):
  page = page - 10
  response = requests.get(f'https://kitsu.io/api/edge/anime?filter%5Bcategories%5D={category}&page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'categories/previous.html', {'response':response, 'category':category,'page':page})

def categories_first(request,category):
  page = 0
  response = requests.get(f'https://kitsu.io/api/edge/anime?filter%5Bcategories%5D={category}&page%5Blimit%5D=9&page%5Boffset%5D={page}').json() ##category will be diff depending on button
  return render(request, 'category.html', {'response': response, 'category':category, 'page':page})

def search(request):
  page = 0
  body = request.POST.get('handle',None)
  response = requests.get(f'https://kitsu.io/api/edge/anime?filter%5Btext%5D={body}&page%5Blimit%5D=12&page%5Boffset%5D={page}').json()
  return render(request, 'search.html', {'response': response, 'body':body, 'page':page})

#still not working sorry
#working now justin
@login_required
def add_comment(request, api_anime_id):
  comments = Comment.objects.filter(anime_id = api_anime_id)
  comment_form = CommentForm()
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json()
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.anime_id = api_anime_id
    new_comment.user_id = request.user.id
    new_comment.save()
  return render(request, 'detail.html', {'response': response, 'api_anime_id':api_anime_id, 'comment_form':comment_form, 'comments':comments})


def random(request):
  api_anime_id = r.randint(0,11000)
  comment_form = CommentForm() 
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json()
  while response == {
  "errors": [
    {
      "title": "Record not found",
      "detail": f"The record identified by {api_anime_id} could not be found.",
      "code": "404",
      "status": "404"
    }
  ]
}:
    api_anime_id = r.randint(0,4292)
    response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json()
  api_anime_img = response['data']['attributes']['posterImage']['small']
  api_anime_name = response['data']['attributes']['canonicalTitle']
  new_anime = Anime(api_anime_id, api_anime_id, api_anime_name, api_anime_img)
  new_anime.save()
  return render(request,'detail.html', {'response':response,'api_anime_id':api_anime_id, 'api_anime_name': api_anime_name, 'comment_form':comment_form})

#Showing most popular animes according to kitsu
def library(request):
  page = 0
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'library.html', {'response':response,'page':page})
  
def next(request, page):
  page = page + 5 # if a user hit the next button then whatever page is currently at +5 to get the new response
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'next.html', {'response':response, 'page': page})

def previous(request, page):
  page = page - 5 #same as next but backward
  
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'previous.html', {'response':response, 'page': page})

def first(request):
  page = '0' #if user hits first page page = 0 
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'library.html',{'response':response, 'page':page})

def last(request):
  page = '16143' # according to api docs 16543 is the last page number
  response = requests.get(f'https://kitsu.io/api/edge/anime?page%5Blimit%5D=9&page%5Boffset%5D={page}').json()
  return render(request, 'library.html',{'response':response, 'page':page})





@login_required
def add_photo(request, profile_id):
    # photo-file will be the "name" attribute on the <input type="file">
    profile = Profile.objects.filter(user=request.user)
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, profile_id=profile_id)
        except:
            print('An error occurred uploading file to S3')
    return render(request, 'profile.html', {'profile_id':profile_id, 'profile':profile})

@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

#if the user is logged in a edit profile form is visible. 
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
      return redirect('profile_create')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_favorite(request, api_anime_id, api_anime_name):
  profile = Profile.objects.filter(user=request.user)
  comments = Comment.objects.filter(anime_id = api_anime_id)
  comment_form = CommentForm()
  anime = Anime.objects.get(id=api_anime_id)
  profile[0].favs.add(anime)
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json() #making new request to api with anime id
  return render(request, 'detail.html', {'response': response, 'api_anime_id':api_anime_id, 'comment_form':comment_form, 'comments':comments})

def delete_favorite(request, anime_api_id):
  profile = Profile.objects.filter(user=request.user)
  anime = Anime.objects.get(id = anime_api_id)
  profile[0].favs.remove(anime)
  return render(request, 'profile.html' ,{'profile': profile})

def delete_comment(request, api_anime_id, comment_id):
  anime = Anime.objects.get(id=api_anime_id)
  comment = Comment.objects.get(id = comment_id)
  comments = Comment.objects.filter(anime_id = api_anime_id)
  response = requests.get(f'https://kitsu.io/api/edge/anime/{api_anime_id}').json()
  comment.delete()
  comment_form = CommentForm() 
  return render(request, 'detail.html', {'response': response, 'api_anime_id':api_anime_id, 'comment_form':comment_form, 'comments':comments})

