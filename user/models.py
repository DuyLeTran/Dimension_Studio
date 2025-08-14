from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from .base import UserManager
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_verify = models.BooleanField(_("is verify"), default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=_("The groups this user belongs to. A user will get all permissions granted to each of their groups."),
        verbose_name=_("groups"),
        related_name='user_groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text=_("Specific permissions for this user."),
        verbose_name=_("user permissions"),
        related_name='user_permissions',
    )

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

class Subscription(models.Model):
    '''
    Model representing subscription plans available in the system.
    '''
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    '''
    Model representing user profile information.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    expired_date = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=20, validators=[MaxValueValidator(20), MinValueValidator(0)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(attempts__gte=0) & models.Q(attempts__lte=20),
                name='attempt must between 0 and 20'
            ),
        ]

    def __str__(self):
        return self.user.email

class PurchaseHistory(models.Model):
    '''
    Purchase history model stored the purchase history of the user.
    '''
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    transaction_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(default=timezone.now)
    expired_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_image = models.ImageField(upload_to='payment_image/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def is_active(self):
        return self.expired_date > timezone.now()

    def __str__(self):
        return f"{self.user.email} - {self.plan} ({self.purchase_date.strftime('%Y-%m-%d')})"

@receiver(pre_save, sender=PurchaseHistory)
def update_profile_on_purchase_success(sender, instance, **kwargs):
    """
    Signal to update profile's subscription and expired_date when purchase status changes to success
    """
    if instance.pk:  # Check if this is an update (not a new purchase)
        try:
            old_instance = PurchaseHistory.objects.get(pk=instance.pk)
            # Check if status changed to success
            if instance.status == 'success' and old_instance.status != 'success':
                # Update purchase dates
                instance.purchase_date = timezone.now()
                instance.expired_date = timezone.now() + timedelta(days=30)

                instance.user.profile.subscription = instance.plan
                instance.user.profile.expired_date = instance.expired_date
                instance.user.profile.save()
        except PurchaseHistory.DoesNotExist:
            pass  # This is a new purchase, no need to update profile

class TryOnHistory(models.Model):
    '''
    Try on history model stored the try on history of the user.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='try_on_history')
    try_on_date = models.DateTimeField(default=timezone.now)
    person_image_url = models.CharField(max_length=500, null=True, blank=True, help_text="Cloud URL of the person image")
    outfit_image_url = models.CharField(max_length=500, null=True, blank=True, help_text="Cloud URL of the outfit image")
    result_image_url = models.CharField(max_length=500, null=True, blank=True, help_text="Cloud URL of the result image")

    def __str__(self):
        return f"{self.user.email} - {self.try_on_date.strftime('%Y-%m-%d %H:%M')}"
    