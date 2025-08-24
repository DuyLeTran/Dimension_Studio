from django.shortcuts import render, redirect
from user.models import Subscription, TryOnHistory
from AI.api_client import API_Client
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def try_on(request):
    attempts = request.user.profile.attempts
    subscription = request.user.profile.subscription
    if request.method == 'POST':
        
        person_image = request.FILES.get('person_image')
        outfit_image = request.FILES.get('outfit_image')

        if subscription.name == 'Premium' or attempts > 0:
            api = API_Client()
            cloud_person_image = api.upload_person_image(person_image)
            cloud_cloth_image = api.upload_cloth_image(outfit_image)
            result_image_path = api.fashion_api_client(cloud_person_image['secure_url'], cloud_cloth_image['secure_url'])

            if subscription.name != 'Premium':
                attempts = attempts - 1 
                request.user.profile.attempts = attempts
                request.user.profile.save()
            
            TryOnHistory.objects.create(
                user=request.user,
                person_image_url=cloud_person_image['secure_url'],
                outfit_image_url=cloud_cloth_image['secure_url'],
                result_image_url=result_image_path[0]
            )
            messages.success(request, 'Try on successfully')
            return render(request, 'TryON.html', {
                'person_image_url': cloud_person_image['secure_url'],
                'outfit_image_url': cloud_cloth_image['secure_url'],
                'result_image_url': result_image_path[0],
                'attempts': attempts,
            })
        else:
            messages.error(request, 'You have no attempts left. Please purchase a subscription.')
            return render(request, 'TryON.html',{'attempts': attempts})

    return render(request, 'TryON.html',{'attempts': attempts})

