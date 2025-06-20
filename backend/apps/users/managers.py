from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def _create_user(self, email, username, password, phone, **extra_fields):
        """
        Private helper method to create and save a user with the given email, username, password, and phone.
        This method is called internally by create_user and create_superuser.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))

        email = self.normalize_email(email)
        
        # Buat user instance dengan semua field yang sudah diekstrak
        # dan sisa extra_fields (seperti is_staff, is_superuser, is_active)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        
        user.set_password(password) # Mengatur dan menghash password
        user.save(using=self._db) # Menyimpan user ke database
        return user

    def create_user(self, email, username, password=None, phone=None, **extra_fields):
        """
        Create and save a regular User with the given email, username, password, and phone.
        By default, sets is_staff=False and is_superuser=False.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True) # Pengguna biasa biasanya aktif secara default
        
        # Meneruskan semua argumen ke _create_user
        return self._create_user(email, username, password, phone, **extra_fields)

    def create_superuser(self, email, username, password=None, phone=None, **extra_fields):
        """
        Create and save a SuperUser with the given email, username, password, and phone.
        Superuser must have is_staff=True, is_superuser=True, and is_active=True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superuser harus selalu aktif

        # Validasi tambahan untuk superuser
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if not username:
            raise ValueError(_('Superuser must have a username.'))

        # Meneruskan semua argumen ke _create_user
        return self._create_user(email, username, password, phone, **extra_fields)