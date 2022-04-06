from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('login',views.Login.as_view(), name='login'),
    path('logout',views.logout, name='logout'),
    path('register',views.Register.as_view(), name='register'),
    path('register_cinema',views.RegisterCinema.as_view(), name='register_cinema'),
    path('bookings',views.bookings, name='bookings'),
    path('profile',views.Profile.as_view(), name='profile'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('add_shows',views.AddShows.as_view(), name='add_shows'),
    path('earnings',views.earnings, name='earnings'),
] 