# apps/common/models.py
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=100, unique=True,
                            help_text=_("Name of the destination category (e.g., Beach, Mountain, Temple)."))
    # Slug bisa ditambahkan jika Anda ingin URL yang lebih ramah untuk kategori
    slug = models.SlugField(_("Slug"), max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(
        # null & blank True jika ditambahkan belakangan
        "Created At"), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(
        # null & blank True jika ditambahkan belakangan
        "Updated At"), null=True, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['-id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Facility(models.Model):
    name = models.CharField(_("Facility Name"), max_length=100, unique=True,
                            help_text=_("Name of the facility (e.g., Parking, Toilet, Wi-Fi)."))
    icon_url = models.CharField(_("Icon URL or Class"), max_length=255, blank=True, null=True,
                                help_text=_("URL to an icon image or a CSS class for an icon font."))
    # Anda bisa menggunakan ImageField jika ikon adalah file gambar yang diupload:
    # icon_image = models.ImageField(upload_to='facility_icons/', blank=True, null=True)

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")
        ordering = ['name']

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(_("Street Address"), max_length=255,
                              help_text=_("Full street address, including house number if applicable."))
    sub_district = models.CharField(_("Sub-District / Village"), max_length=100, blank=True, null=True,
                                    help_text=_("e.g., Kelurahan, Desa."))
    # ERD Anda tidak memiliki 'district' (kecamatan), tapi saya tambahkan sebagai contoh jika diperlukan
    # district = models.CharField(_("District"), max_length=100, blank=True, null=True, help_text=_("e.g., Kecamatan."))
    regency = models.CharField(_("Regency / City"), max_length=100,
                               help_text=_("e.g., Kabupaten Badung, Kota Denpasar."))
    # ERD Anda tidak memiliki 'province' dan 'country', tapi ini field yang umum.
    # province = models.CharField(_("Province"), max_length=100, default="Bali")
    # country = models.CharField(_("Country"), max_length=100, default="Indonesia")
    # postal_code = models.CharField(_("Postal Code"), max_length=10, blank=True, null=True)
    latitude = models.DecimalField(
        _("Latitude"), max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(
        _("Longitude"), max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        # Pertimbangkan untuk membuat Address unik berdasarkan kombinasi field jika diperlukan
        # unique_together = [['street', 'regency', 'latitude', 'longitude']]

    def __str__(self):
        parts = [self.street, self.sub_district, self.regency]
        return ", ".join(filter(None, parts)) or "Unnamed Address"


class Contact(models.Model):
    phone = models.CharField(
        _("Phone Number"), max_length=25, blank=True, null=True)
    # Di ERD Anda namanya 'mail', standar Django 'email'
    mail = models.EmailField(_("Email Address"), blank=True, null=True)
    # website = models.URLField(_("Website URL"), blank=True, null=True) # Field website umum ditambahkan

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.mail or self.phone or "Unnamed Contact"
