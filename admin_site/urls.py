from django.urls import path
from . import views

app_name = 'admin_site'

urlpatterns = [
    path('', views.admin_homepage, name='admin_homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('transaction-queue/', views.transaction_queue, name='transaction_queue'),
    path('transaction/<str:transaction_id>/update-status/', views.update_transaction_status, name='update_transaction_status'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('subscription-management/', views.subscription_management, name='subscription_management'),

    # path('test/', views.test, name='test'),
]   