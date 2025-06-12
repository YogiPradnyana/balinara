from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Private helper method to create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        # Mengubah domain email menjadi huruf kecil
        email = self.normalize_email(email)
        # Anda bisa menambahkan validasi username di sini jika username adalah field yang wajib
        # if 'username' not in extra_fields or not extra_fields.get('username'):
        #     raise ValueError(_('The Username must be set'))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Menangani hashing password
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # Role default bisa diatur di sini atau di model, atau diterima dari extra_fields
        # extra_fields.setdefault('role', 'user')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Superuser harus selalu aktif
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Pastikan username ada untuk superuser, karena itu REQUIRED_FIELD
        if 'username' not in extra_fields or not extra_fields.get('username'):
            # Anda bisa membuat username default atau menaikkan error
            # Contoh: extra_fields.setdefault('username', email.split('@')[0] + '_admin')
            raise ValueError(_('Superuser must have a username.'))

        return self._create_user(email, password, **extra_fields)
