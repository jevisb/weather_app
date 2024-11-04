# weather/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.BASE, name='home'),  # URL route to display home.html
    path('current-weather/', views.get_current_weather, name='current_weather'),
    path('forecast/', views.get_forecast, name='forecast'),
    path('search-history/', views.search_history, name='search_history'),
]
