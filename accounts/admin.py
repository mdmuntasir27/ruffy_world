from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at',)


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom UserAdmin that prevents administrators from resetting or changing user passwords.
    Password recovery/changes can only be performed by users themselves.
    """
    change_password_form = None

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        # Exclude password field from the change form
        return (
            (None, {'fields': ('username',)}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
        )

    def get_urls(self):
        urls = super().get_urls()
        # Remove password change URL from admin
        return [url for url in urls if 'password' not in str(getattr(url, 'pattern', ''))]

    def user_change_password(self, request, id, form_url=''):
        raise PermissionDenied("Password reset in the admin panel is disabled. Password reset must be initiated by users.")
