from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from user.models import User, Profile, Subscription
from django.db.models import Q
import os



class CleanUnverifiedUsersMiddleware:
    '''
    Middleware to clean unverified users older than 20 minutes.
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.clean_unverified_users()
        response = self.get_response(request)
        return response

    def clean_unverified_users(self):
        threshold = timezone.now() - timedelta(minutes=20)
        unverified_users = User.objects.filter(is_verify=False, date_joined__lt=threshold)

        if unverified_users.exists():
            with open(settings.BASE_DIR /'log'/ 'delete.log', 'a') as f:
                for user in unverified_users:
                    f.write(
                        f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}, {user.pk} - INFO - Email: {user.email} - REASON: Verification time expired\n'
                    )

            unverified_users.delete()


class AutoDowngradeMiddleware:
    """
    Middleware automatically downgrades expired users to the Free plan,
    and logs each downgrade.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.downgrade_expired_subscriptions()
        return self.get_response(request)

    def downgrade_expired_subscriptions(self):
        now = timezone.now()
        try:
            free_plan = Subscription.objects.get(name__iexact='Free')
        except Subscription.DoesNotExist:
            return  # Không có gói Free thì bỏ qua

        expired_profiles = Profile.objects.filter(
            Q(subscription__isnull=False) & 
            Q(expired_date__lt=now) & 
            ~Q(subscription=free_plan)
        )

        if expired_profiles.exists():
            log_path = os.path.join(settings.BASE_DIR, 'log', 'downgrade.log')
            with open(log_path, 'a') as log_file:
                for profile in expired_profiles:
                    log_file.write(
                        f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"User: {profile.user.email} downgraded from '{profile.subscription.name}' to 'Free' (expired on {profile.expired_date})\n"
                    )
                    profile.subscription = free_plan
                    profile.expired_date = timezone.now() + timedelta(days=30)
                    profile.save()

class ResetFreePlanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.reset_free_plan_attempts()
        return self.get_response(request)
    
    def reset_free_plan_attempts(self):
        now = timezone.now()
        free_plan = Subscription.objects.get(name__iexact='Free')

        free_plan_profiles = Profile.objects.filter(
            Q(subscription=free_plan) &
            Q(expired_date__lt=now)
        )

        if free_plan_profiles.exists():
            for profile in free_plan_profiles:
                with open(settings.BASE_DIR / 'log' / 'reset_free_plan.log', 'a') as f:
                    f.write(
                        f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}, {profile.user.email} - INFO - Reset free plan attempts\n'
                    )
                profile.attempts = 20
                profile.expired_date = now + timedelta(days=30)
                profile.save()
