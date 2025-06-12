from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # Menggunakan model User kustom Anda
from .forms import UserCreationFormAdmin, UserChangeFormAdmin  # Form admin kustom


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeFormAdmin
    add_form = UserCreationFormAdmin

    model = User
    list_display = ['email', 'username',
                    'phone', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['email', 'username', 'phone']
    ordering = ['email']

    # Fieldsets di-override dari BaseUserAdmin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',
         'date_joined', 'updated_at', 'email_verified_at')}),
    )
    # Fieldset untuk halaman tambah user baru
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password2', 'phone', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined',
                       'updated_at', 'email_verified_at')
