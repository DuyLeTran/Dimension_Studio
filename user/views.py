from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.translation import gettext_lazy as _
from .models import User, Profile, Subscription, PurchaseHistory
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember', False)
        print(remember_me)
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_verify:
            auth_login(request, user)
            if remember_me:
                request.session.set_expiry(1209600) # 2 weeks
            else:
                # Set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
                request.session.set_expiry(0)
            return redirect('home:home')
        elif user and not user.is_verify:
            error = _('Please check your email to activate your account')
            return render(request, 'authentication/login.html', {'error': error})
        else:
            error = _('Invalid email or password')
            return render(request, 'authentication/login.html', {'error': error})
    return render(request, 'authentication/login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        verify_password = request.POST['verify_password']
        if User.objects.filter(email=email).exists():
            error = _('Email already exists')
            return render(request, 'authentication/register.html', {'error': error})
        if password == verify_password: 
            user = User.objects.create_user(email=email, password=password, is_verify=False)

            # tạo uid và token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            
            # tạo đường dẫn xác thực
            activation_link = request.build_absolute_uri(
                reverse('user:activate', kwargs={'uidb64': uid, 'token': token})
            )

            send_mail(
                subject='Xác minh tài khoản Dimension Studio',
                message=f'Nhấn vào link sau để kích hoạt tài khoản:\n{activation_link}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'authentication/verify_wait.html')
            # return redirect('home:home')
    return render(request, 'authentication/register.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verify = True
        user.save()
        profile = Profile.objects.create(user=user, subscription=Subscription.objects.get(name='Free'), expired_date=timezone.now() + timedelta(days=30))
        auth_login(request, user)
        return redirect('home:home')
    else:
        return HttpResponse("Liên kết không hợp lệ hoặc đã hết hạn. Vui lòng đăng ký lại.")

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_verify:
                # Tạo token reset password
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                
                # Tạo link reset password
                reset_link = request.build_absolute_uri(
                    reverse('user:reset_password', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Gửi email
                send_mail(
                    subject='Đặt lại mật khẩu Dimension Studio',
                    message=f'Nhấn vào link sau để đặt lại mật khẩu:\n{reset_link}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Link đặt lại mật khẩu đã được gửi đến email của bạn.')
            else:
                messages.error(request, 'Tài khoản chưa được xác thực. Vui lòng xác thực tài khoản trước.')
        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy tài khoản với email này.')
        return redirect('user:forgot_password')
    return render(request, 'authentication/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Mật khẩu đã được đặt lại thành công. Vui lòng đăng nhập lại.')
                return redirect('user:login')
            else:
                messages.error(request, 'Mật khẩu xác nhận không khớp.')
        return render(request, 'authentication/reset_password.html')
    else:
        messages.error(request, 'Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.')
        return redirect('user:forgot_password')

def logout(request):
    auth_logout(request)
    return redirect('home:home')

@login_required
def profile(request):
    if request.method == 'POST':
        if 'reset' in request.POST:
            print('reset')
        # Update user info
        user = request.user
        full_name = request.POST.get('full_name', '').split()
        if len(full_name) > 0:
            user.first_name = full_name[0]
            user.last_name = ' '.join(full_name[1:]) if len(full_name) > 1 else ''
        user.save()

        # Update profile
        profile = user.profile
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.phone = request.POST.get('phone')
        profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('user:profile')

    return render(request, 'account setting/profile.html')

@login_required
def security(request):
    return render(request, 'account setting/security.html')

@login_required
def purchase_history(request):
    purchases = PurchaseHistory.objects.filter(user=request.user)   
    return render(request, 'account setting/purchase_history.html', {'purchases': purchases})

@login_required
def payment(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    purchase = PurchaseHistory.objects.filter(user=request.user, plan=subscription)
    if request.method == 'POST':
        payment_image = request.FILES.get('payment_image')

        if payment_image:
            # Create purchase history record
            purchase = PurchaseHistory.objects.create(
                user=request.user,
                plan=subscription,
                purchase_date=timezone.now(),
                expired_date=timezone.now() + timedelta(days=30),
                price=subscription.price,
                status='processing'
            )
            
            # Get file extension
            file_extension = payment_image.name.split('.')[-1]
            # Create new filename using transaction_id
            new_filename = f"{purchase.transaction_id}.{file_extension}"
            # Save payment image with transaction ID as filename
            purchase.payment_image.save(new_filename, payment_image, save=True)
            
            messages.success(request, 'Payment image uploaded successfully')
        return redirect('user:purchase_history')
    
    return render(request, 'account setting/payment.html', {
        'subscription': subscription
    })
