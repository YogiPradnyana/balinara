import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils.text import slugify
# Create your models here.


def user_image_path(instance, filename):
    # file akan diupload ke MEDIA_ROOT/user_images/user_<id>_<username>/<filename>
    # Pastikan instance.username aman atau gunakan instance.id
    ext = filename.split('.')[-1]
    # Gunakan ID jika sudah ada untuk path yang lebih stabil, atau UUID untuk kasus lain
    identifier = instance.pk if instance.pk else uuid.uuid4()
    # Slugify username untuk nama file yang aman
    safe_username = slugify(instance.username) if instance.username else "user"
    new_filename = f'{identifier}_{safe_username}.{ext}'
    return f'user_images/{new_filename}'

    # Pertimbangkan menggunakan yang atas atau bawah

    # return f'user_images/user_{instance.id}_{instance.username}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', _('Admin')),
        ('user', _('User (Traveler)')),
    ]

    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    # Password akan dihandle oleh AbstractBaseUser
    phone = models.CharField(
        _('phone number'), max_length=20, blank=True, null=True)
    role = models.CharField(_('role'), max_length=20,
                            choices=ROLE_CHOICES, default='user')
    image = models.ImageField(_('profile image'),
                              upload_to=user_image_path, null=True, blank=True)
    email_verified_at = models.DateTimeField(_('email verified at'),
                                             null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated_at = models.DateTimeField(_('last updated'), auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Field utama untuk login
    # Field yang diminta saat `createsuperuser` selain email & password
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']  # Contoh urutan default

    def __str__(self):
        return self.email
