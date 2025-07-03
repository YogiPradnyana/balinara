# apps/users/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Pastikan Anda memiliki CustomUserManager di 'apps/users/managers.py'
# Contoh import:
from .managers import CustomUserManager 


def user_image_path(instance, filename):
    """
    Menghasilkan path unik untuk upload gambar profil pengguna.
    Gambar akan disimpan di MEDIA_ROOT/user_images/<uuid_id_username>.<ext>
    """
    ext = filename.split('.')[-1].lower() # Ambil ekstensi file dan ubah ke huruf kecil
    
    # Gunakan PK (ID) pengguna jika sudah ada, jika belum (saat membuat user baru), pakai UUID sementara.
    # Ini penting karena instance.id mungkin belum tersedia sebelum save pertama.
    identifier = instance.pk if instance.pk else uuid.uuid4() 
    
    # Slugify username untuk nama file yang aman dan mudah dibaca
    # Fallback ke 'unknown_user' jika username belum ada
    safe_username = slugify(instance.username) if instance.username else "unknown_user"
    
    new_filename = f'user_{identifier}_{safe_username}.{ext}'
    return f'user_images/{new_filename}'


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model User kustom yang menggabungkan AbstractBaseUser dan PermissionsMixin.
    Menggunakan email sebagai USERNAME_FIELD untuk login.
    """
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    # Password akan dihandle secara otomatis oleh AbstractBaseUser

    phone = models.CharField(
        _('phone number'), 
        max_length=20, 
        blank=True, 
        null=True,
        help_text=_("User's contact phone number.")
    )
    image = models.ImageField(
        _('profile image'),
        upload_to=user_image_path, 
        null=True, 
        blank=True,
        help_text=_("Upload a profile image for the user.")
    )
    email_verified_at = models.DateTimeField(
        _('email verified at'),
        null=True, 
        blank=True,
        help_text=_("Timestamp when the user's email was verified.")
    )
    is_staff = models.BooleanField(
        _('staff status'), 
        default=False,
        help_text=_("Designates whether the user can log into this admin site.")
    )
    is_active = models.BooleanField(
        _('active'), 
        default=True,
        help_text=_("Designates whether this user should be treated as active. "
                    "Unselect this instead of deleting accounts.")
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated_at = models.DateTimeField(_('last updated'), auto_now=True)

    # --- DEFINISI FIELD ROLE DENGAN PILIHAN BARU ---
    ROLE_CHOICES = (
        ('admin', 'Admin'),      # Admin users
        ('traveler', 'Traveler'), # Regular users / travelers
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='traveler', # Default role saat user baru dibuat
        help_text=_('Designates the role of the user within the application.')
    )
    # --- AKHIR DEFINISI FIELD ROLE ---

    # Menggunakan CustomUserManager untuk manajemen user kustom
    objects = CustomUserManager() 

    USERNAME_FIELD = 'email'  # Field yang digunakan untuk login (harus unik)
    # Field yang akan diminta saat menjalankan `createsuperuser` selain USERNAME_FIELD dan password
    REQUIRED_FIELDS = ['username', 'role'] 

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']  # Urutan default untuk query user

    def __str__(self):
        return self.email # Representasi string objek User (misalnya di admin)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # --- PERUBAHAN LOGIKA SAVE() UNTUK is_staff ---
    def save(self, *args, **kwargs):
        """
        Custom save method to manage `is_staff` based on `role`.
        Ensures that `is_superuser` status is maintained.
        """
        # Jika user adalah superuser, mereka HARUS selalu is_staff = True
        if self.is_superuser:
            self.is_staff = True
        # Jika user bukan superuser, tentukan is_staff berdasarkan field 'role'
        elif self.role == 'admin':
            self.is_staff = True
        else:
            self.is_staff = False # Untuk 'traveler' atau role lain yang mungkin ditambahkan

        super().save(*args, **kwargs)
    # --- AKHIR PERUBAHAN LOGIKA SAVE() ---

    # Metode-metode PermissionsMixin, perlu diimplementasikan
    # is_superuser dari PermissionsMixin sudah menangani sebagian besar izin
    def has_perm(self, perm, obj=None):
        """
        Mengembalikan True jika pengguna memiliki izin yang ditentukan.
        Sederhana: superuser selalu punya izin, admin punya izin jika is_staff True.
        """
        return self.is_active and (self.is_superuser or self.is_staff) # Jika admin, is_staff sudah diatur True

    def has_module_perms(self, app_label):
        """
        Mengembalikan True jika pengguna memiliki izin untuk melihat modul aplikasi yang ditentukan.
        """
        return self.is_active and (self.is_superuser or self.is_staff)