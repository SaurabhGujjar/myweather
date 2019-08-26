from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<city_name>/', views.delete, name='delete'),
    path('loc_weather/', views.location, name='location'),
]