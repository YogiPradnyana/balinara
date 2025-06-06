# apps/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # Model User kustom Anda


class UserCreationFormAdmin(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Fields yang akan muncul di form pembuatan user di admin
        # 'password2' akan di-handle oleh UserCreationForm
        fields = ('email', 'username', 'phone', 'role',
                  'is_staff', 'is_superuser', 'is_active')


class UserChangeFormAdmin(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        # Fields yang akan muncul di form edit user di admin
        fields = ('email', 'username', 'phone', 'role', 'image', 'is_active', 'is_staff',
                  'is_superuser', 'groups', 'user_permissions', 'email_verified_at')
