from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User

__all__ = (
    'UserAdmin',
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """User admin.

    Admin class definitions for ``User`` model.

    """
    search_fields = ('first_name', 'last_name', 'email')
    list_display = (
        'id',
        'email',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
        'is_superuser'
    )
    list_display_links = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = DjangoUserAdmin.readonly_fields + (
        'last_login',
        'date_joined',
    )
    ordering = ('email',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
