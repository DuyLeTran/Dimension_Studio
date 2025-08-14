from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('profile/', views.profile, name='profile'),
    path('security/', views.security, name='security'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),
    path('payment/<int:subscription_id>/', views.payment, name='payment'),
    path('try-on-history/', views.try_on_history, name='try_on_history'),
]