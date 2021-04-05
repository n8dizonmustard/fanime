from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('random/', views.random, name='random'),
    path('library/', views.library, name="library"),
    path('categories/<str:category>', views.categories, name ='categories'), ##<str:category> is gonna come from the button they click
    path('categories/<str:category>/next/<int:page>', views.categories_next, name='categories_next'),
    path('next/<int:page>', views.next, name='next'),
    path('previous/<int:page>', views.previous, name ='previous'),
    path('first/', views.first, name ='first'),
    path('last/', views.last, name ='last'),
    path('detail/<int:api_anime_id>', views.detail, name='detail'),
    path('detail/<int:api_anime_id>', views.add_comment, name ='add_comment'), 
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.ProfileCreate.as_view(), name="profile_create"),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name="profile_update"),
    path('profile/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]