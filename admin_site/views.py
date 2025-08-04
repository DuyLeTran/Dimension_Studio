from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import User, PurchaseHistory, Subscription
from django.core.paginator import Paginator
from django.db.models import Case, When, Value, IntegerField, Q, Sum
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone

def is_admin(user):
    return user.is_superuser   

@login_required
@user_passes_test(is_admin)
def admin_homepage(request):
    return redirect('admin_site:dashboard')

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    active_subscriptions = User.objects.filter(
        Q(profile__subscription__name__iexact = 'Plus') |
        Q(profile__subscription__name__iexact = 'Premium')
    ).count() 
    # print(users.filter(Q(profile__subscription__name__iexact='Free') & Q(profile__expired_date__gte=timezone.now())))
    # print(users.profile.subscription.name)
    context = {
        'users': User.objects.all() ,
        'subscriptions': Subscription.objects.all(),
        'purchases': PurchaseHistory.objects.all(),
        'active_subscriptions': active_subscriptions, # total active subscriptions
    }
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.all() 
    subscriptions = Subscription.objects.all()
    role = request.GET.get('role', '') 
    subscription = request.GET.get('subscription', '')
    phone = request.GET.get('search_phone', '')
    email = request.GET.get('search_email', '')
    name = request.GET.get('search_name', '')
    expired_date = request.GET.get('expired_date', '')
    # paginator = Paginator(users, 10)  # Show 10 items per page
    # page = request.GET.get('page', 1)
    # users = paginator.get_page(page)    

    # tan = User.objects.get(email = 'tannnsse180203@fpt.edu.vn')
    # print(tan.profile.subscription.name)

    if role:
        if role == 'Admin':
            users = users.filter(is_superuser=True)
        elif role == 'Staff':
            users = users.filter(is_staff=True, is_superuser=False)
        elif role == 'User':
            users = users.filter(is_staff=False, is_superuser=False)
    if subscription:
        users = users.filter(profile__subscription=subscription)
    if expired_date:
        users = users.filter(profile__expired_date__gte=expired_date)
    if phone:
        users = users.filter(profile__phone__icontains=phone)
    if email:
        users = users.filter(email__icontains=email)
    if name:
        users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
    context = {
        'users': users,
        'subscriptions': subscriptions
    }
    return render(request, 'user_management.html', context)
@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        attempt = request.POST.get('attempt')
        phone = request.POST.get('phone')
        subscription_id = request.POST.get('subscription')
        role = request.POST.get('role')


        try:
            # Update user fields
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Update profile fields
            profile = user.profile
            profile.phone = phone
            profile.attempt = attempt
            if subscription_id:
                profile.subscription = Subscription.objects.get(id=subscription_id)
            
            profile.full_clean()
            profile.save()

            # Update role
            if role == 'Staff':
                user.is_staff = True
                user.is_superuser = False
            elif role == 'User':
                user.is_staff = False
                user.is_superuser = False
            user.save()

            messages.success(request, 'User updated successfully')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')

        return redirect('admin_site:user_management')
    return redirect('admin_site:user_management')

@login_required 
@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.method == 'POST':
        try:    
            user = User.objects.get(id=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
        return redirect('admin_site:user_management')
    return redirect('admin_site:user_management') 

@login_required
@user_passes_test(is_admin)
def transaction_queue(request):
    # Get filter parameters
    status = request.GET.get('status', '')
    plan_id = request.GET.get('plan', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    email = request.GET.get('search_email', '')
    transaction_id = request.GET.get('search_transaction_id', '')
    
    # Base queryset
    purchases = PurchaseHistory.objects.all().select_related('user', 'plan').order_by('-purchase_date')
    '''
    This function is used to sort the purchases by status = 'processing' priority.
    If status is not 'processing', it will be sorted by purchase_date.
    If status is 'processing', it will be sorted by purchase_date.

    purchases = PurchaseHistory.objects.annotate(
        status_priority=Case(
            When(status='processing', then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).select_related('user', 'plan').order_by('status_priority', '-purchase_date')
    '''
    
    # Apply filters
    if status:
        purchases = purchases.filter(status=status)
    if plan_id:
        purchases = purchases.filter(plan_id=plan_id)
    if date_from:
        purchases = purchases.filter(purchase_date__gte=datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        purchases = purchases.filter(purchase_date__lte=datetime.strptime(date_to, '%Y-%m-%d'))
    if email:
        purchases = purchases.filter(user__email__icontains=email)
    if transaction_id:
        purchases = purchases.filter(transaction_id__icontains=transaction_id)
        
    # Pagination
    paginator = Paginator(purchases, 10)  # Show 10 items per page
    page = request.GET.get('page', 1)
    purchases = paginator.get_page(page)
    
    # Get all plans for filter
    plans = Subscription.objects.all()
    
    # Get status choices
    status_choices = PurchaseHistory.STATUS_CHOICES
    
    context = {
        'purchases': purchases,
        'plans': plans,
        'status_choices': status_choices,
    }
    
    return render(request, 'transaction_queue.html', context)

@login_required
@user_passes_test(is_admin)
def update_transaction_status(request, transaction_id):
    if request.method == 'POST':
        try:
            purchase = PurchaseHistory.objects.get(transaction_id=transaction_id)
            new_status = request.POST.get('status')
            
            if new_status in dict(PurchaseHistory.STATUS_CHOICES):
                purchase.status = new_status
                purchase.save()
                return redirect('admin_site:transaction_queue')
            else:
                return redirect('admin_site:transaction_queue')
        except PurchaseHistory.DoesNotExist:
            return redirect('admin_site:transaction_queue')
    return redirect('admin_site:transaction_queue')

@login_required
@user_passes_test(is_admin)
def subscription_management(request):
    subscriptions = Subscription.objects.all()

    if request.method == 'POST':
        plan_type = request.POST.get('planType','')
        plan_name = request.POST.get('planName')
        plan_price = request.POST.get('planPrice')
        plan_description = request.POST.get('planDescription')
        popular_plan_id = request.POST.get('popular_plan_id',False)
        if popular_plan_id:
            try:    
                popular_plan = Subscription.objects.get(id=popular_plan_id)
                popular_plan.is_popular = True
                popular_plan.save()
                
            except Subscription.DoesNotExist:
                messages.error(request, 'Popular plan not found')
                return redirect('admin_site:subscription_management')

            for subscription in subscriptions:
                if subscription.name != popular_plan.name:
                    subscription.is_popular = False
                    print('subscription.id:',subscription.id, 'popular_plan_id:',popular_plan_id, 'subscription:',subscription.name, 'subscription.is_popular:',subscription.is_popular)
                    subscription.save()

            messages.success(request, 'Popular plan updated successfully')
            return redirect('admin_site:subscription_management')
        try:
            subscription = Subscription.objects.get(name__iexact=plan_type)

            subscription.name = plan_name
            subscription.price = plan_price
            subscription.description = plan_description
            subscription.save()
            messages.success(request, f'{plan_name} subscription updated successfully')
            return redirect('admin_site:subscription_management')
        except Subscription.DoesNotExist:
            print('plan_type:',plan_type)
            messages.error(request, 'Subscription not found')
            return redirect('admin_site:subscription_management')
    return render(request, 'subscription_management.html', {'subscriptions': subscriptions})