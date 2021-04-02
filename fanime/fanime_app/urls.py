from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('detail/', views.detail, name='detail'),
    path('profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
]