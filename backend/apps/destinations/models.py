# apps/destinations/models.py
import uuid
from django.db import models
# Untuk AUTH_USER_MODEL jika ingin melacak pembuat
from django.conf import settings
# Jarang dipakai langsung di sini, lebih ke auto_now_add
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Impor model dari aplikasi 'common'
# Pastikan Django bisa menemukan path ini. Jika 'apps' adalah root source Anda, maka ini benar.
from apps.common.models import Category, Address, Contact, Facility

# Fungsi untuk path upload gambar destinasi


def destination_image_path_processor(instance, filename):
    # Ambil ekstensi dan jadikan lowercase
    ext = filename.split('.')[-1].lower()
    # Buat nama file yang unik menggunakan UUID untuk DestinationImage
    new_filename = f'{uuid.uuid4()}.{ext}'
    # Simpan dalam subfolder berdasarkan ID atau slug destinasi (pastikan instance.destination ada)
    # instance di sini adalah DestinationImage, jadi kita akses instance.destination.id
    destination_identifier = instance.destination.slug if instance.destination.slug else instance.destination.id
    return f'destination_images/dest_{destination_identifier}/{new_filename}'


class Destination(models.Model):
    name = models.CharField(_("Destination Name"), max_length=255,
                            help_text=_("The official name of the destination."))
    slug = models.SlugField(_("Slug"), max_length=270, unique=True, blank=True,
                            help_text=_("A URL-friendly version of the name. Leave blank to auto-generate."))
    description = models.TextField(_("Description"),
                                   help_text=_("A detailed description of the destination."))
    ticket_price_range = models.CharField(
        _("Ticket Price Range"), max_length=100, blank=True, null=True,
        help_text=_("e.g., Rp 50.000 - Rp 100.000, Free, or Starting from Rp 25.000"))
    operational_hours = models.CharField(
        _("Operational Hours"), max_length=150, blank=True, null=True,
        help_text=_("e.g., 08:00 - 17:00 (Daily), 09:00 - 15:00 (Weekends only)"))

    # Field untuk rating dan review (akan diupdate oleh logika lain, misal signals dari Review)
    average_rating = models.DecimalField(
        _("Average Rating"), max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(_("Total Reviews"), default=0)

    # Relasi ke model di aplikasi 'common'
    category = models.ForeignKey(
        Category,
        related_name='destinations',  # Cara mengakses destinasi dari objek Category
        on_delete=models.SET_NULL,   # Jika kategori dihapus, set field ini ke NULL
        null=True,
        blank=True,
        verbose_name=_("Category")
    )
    address = models.OneToOneField(  # Satu destinasi memiliki satu alamat utama
        Address,
        # Atau models.CASCADE jika alamat harus ada dan dihapus bersama destinasi
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # Alamat bisa diisi nanti
        verbose_name=_("Address")
    )
    contact = models.OneToOneField(  # Satu destinasi memiliki satu kontak utama
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # Kontak bisa diisi nanti
        verbose_name=_("Contact Information")
    )
    facilities = models.ManyToManyField(
        Facility,
        # Cara mengakses destinasi dari objek Facility
        related_name='destinations_with_facility',
        blank=True,  # Destinasi bisa saja tidak memiliki fasilitas yang terdaftar
        verbose_name=_("Facilities")
    )

    # Opsional: Siapa yang membuat/mengupdate (jika relevan)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_destinations', on_delete=models.SET_NULL, null=True, blank=True)
    # last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_destinations', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Updated"), auto_now=True)
    is_published = models.BooleanField(
        _("Is Published"), default=False,
        help_text=_("Check if the destination is ready to be shown to users."))

    class Meta:
        verbose_name = _("Destination")
        verbose_name_plural = _("Destinations")
        # Urutkan destinasi berdasarkan nama secara default
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Buat slug otomatis jika kosong
            self.slug = slugify(self.name)
            # Pastikan slug unik jika nama bisa duplikat
            original_slug = self.slug
            queryset = Destination.objects.all().exclude(id=self.id)
            counter = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination,
        # Cara mengakses gambar dari objek Destination (destination.images.all())
        related_name='images',
        on_delete=models.CASCADE,  # Jika destinasi dihapus, gambar terkait juga dihapus
        verbose_name=_("Destination")
    )
    image = models.ImageField(
        _("Image File"),
        # Menggunakan fungsi path yang sudah didefinisikan
        upload_to=destination_image_path_processor,
        help_text=_("Upload an image for the destination.")
    )
    alt_text = models.CharField(
        _("Alt Text"), max_length=255, blank=True, null=True,
        help_text=_("A short description of the image for accessibility and SEO."))
    is_primary = models.BooleanField(
        _("Is Primary Image"), default=False,
        help_text=_("Set one image as the primary display image for the destination."))
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Destination Image")
        verbose_name_plural = _("Destination Images")
        # Tampilkan primary dulu, lalu yang terbaru, lalu berdasarkan urutan upload
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f"Image for {self.destination.name} ({self.alt_text or self.image.name})"

    def save(self, *args, **kwargs):
        # Pastikan hanya ada satu gambar primary per destinasi
        if self.is_primary:
            # Set semua gambar lain untuk destinasi ini menjadi bukan primary
            DestinationImage.objects.filter(destination=self.destination, is_primary=True)\
                                    .exclude(pk=self.pk)\
                                    .update(is_primary=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Hapus file fisik dari storage saat objek gambar dihapus
        # Ini adalah praktik yang baik untuk menjaga kebersihan storage
        if self.image:
            # save=False agar tidak mencoba save model lagi
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
