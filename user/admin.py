from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as djangoUserAdmin
from .models import User, Profile, Subscription, PurchaseHistory
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# Register your models here.

class UserAdmin(djangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_superuser','date_joined','last_login','is_verify')
    list_filter = ('email', 'is_staff', 'date_joined')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_superuser','is_verify')}
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verify",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Subscription)

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'plan', 'purchase_date', 'expired_date', 'priced', 'colored_status')
    # list_filter = ('status', 'plan', 'purchase_date')
    search_fields = ('transaction_id', 'user__email')
    readonly_fields = ('transaction_id',)

    def priced(self, obj):
        try:
            return "{:,.0f}".format(obj.price).replace(",", ".")
        except:
            return obj.price      
    priced.short_description = 'Price'

    def colored_status(self, obj):
        colors = {
            'processing': 'orange',
            'success': 'green',
            'failed': 'red'
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 4px 8px; border-radius: 5px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display() if hasattr(obj, 'get_status_display') else obj.status
        )
    colored_status.short_description = 'Status'
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)