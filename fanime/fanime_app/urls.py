from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('next/<int:page>', views.next, name='next'),
    path('detail/<int:i_id>', views.detail, name='detail'),
    path('profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
]