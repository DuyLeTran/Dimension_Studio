from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('about_us',views.aboutUs, name='about_us'),
    path('application', views.application, name='application'),
    path('resources', views.resources, name='resources'),
    path('pricing', views.pricing, name='pricing'),
    path('how-it-works', views.how_it_works, name='how_it_works'),
]