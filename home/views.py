from django.shortcuts import render
from django.conf import settings
from user.models import Subscription

def home(request):
    return render(request, 'home.html')
def aboutUs(request):
    return render(request, 'aboutUs.html')
def application(request):
    return render(request, 'application.html')
def resources(request):
    return render(request, 'resources.html')
def pricing(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'pricing.html', {'subscriptions': subscriptions})
def how_it_works(request):
    return render(request, 'how_it_work.html')