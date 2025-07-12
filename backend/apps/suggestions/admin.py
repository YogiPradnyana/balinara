from django.contrib import admin
from django.db import transaction
from .models import Suggestion, SuggestionPhoto
from apps.destinations.models import Destination, DestinationImage as DestinationImageModel
from apps.common.models import Address, Contact


class SuggestionPhotoInline(admin.TabularInline):
    """Memungkinkan kita melihat/menambah foto suggestion langsung di halaman admin Suggestion."""
    model = SuggestionPhoto
    extra = 1 # Tampilkan 1 slot upload kosong
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.html import mark_safe
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.action(description='Approve selected suggestions and create destinations')
def approve_suggestion(modeladmin, request, queryset):
    """
    Action untuk menyetujui suggestion. Ini akan:
    1. Membuat objek Address dan Contact baru dari data suggestion.
    2. Membuat objek Destination baru.
    3. Memetakan semua data dari Suggestion ke Destination.
    4. Menyalin semua foto.
    5. Mengubah status Suggestion menjadi 'approved'.
    """
    suggestions_to_approve = queryset.filter(status='pending')

    for suggestion in suggestions_to_approve:
        try:
            # Gunakan transaction.atomic untuk memastikan semua operasi berhasil atau tidak sama sekali
            with transaction.atomic():
                # LANGKAH 1: Buat objek Address dan Contact terlebih dahulu (jika ada data)
                new_address = None
                if suggestion.street or suggestion.regency or suggestion.latitude:
                    new_address = Address.objects.create(
                        street=suggestion.street,
                        sub_district=suggestion.sub_district,
                        regency=suggestion.regency,
                        latitude=suggestion.latitude,
                        longitude=suggestion.longitude
                    )

                new_contact = None
                if suggestion.phone_number or suggestion.email:
                    new_contact = Contact.objects.create(
                        phone_number=suggestion.phone_number,
                        email=suggestion.email
                    )

                # LANGKAH 2: Format rentang harga tiket
                price_range = ""
                min_price = suggestion.entrance_ticket_min
                max_price = suggestion.entrance_ticket_max
                if min_price and max_price:
                    price_range = f"Rp {int(min_price):,} - Rp {int(max_price):,}"
                elif min_price:
                    price_range = f"Starting from Rp {int(min_price):,}"
                elif max_price:
                    price_range = f"Up to Rp {int(max_price):,}"

                # LANGKAH 3: Buat objek Destination utama
                destination = Destination.objects.create(
                    name=suggestion.name,
                    description=suggestion.descriptions,
                    ticket_price_range=price_range,
                    address=new_address,  # Tautkan ke Address yang baru dibuat
                    contact=new_contact,  # Tautkan ke Contact yang baru dibuat
                    is_published=True     # Langsung publish saat disetujui
                )

                # LANGKAH 4: Set relasi Many-to-Many
                # Tambahkan category dari Suggestion ke M2M field di Destination
                if suggestion.category:
                    destination.categories.add(suggestion.category)
                
                # Salin semua fasilitas
                destination.facilities.set(suggestion.facilities.all())

                # LANGKAH 5: Salin semua foto dari SuggestionPhoto ke DestinationImage
                is_first_image = True
                for photo in suggestion.photos.all():
                    DestinationImageModel.objects.create(
                        destination=destination,
                        image=photo.image,
                        alt_text=f"Image for {destination.name}",
                        # Set gambar pertama sebagai primary image
                        is_primary=is_first_image 
                    )
                    is_first_image = False

                # LANGKAH 6: Update status suggestion menjadi 'approved'
                suggestion.status = 'approved'
                suggestion.save()
            
            # Jika berhasil, tampilkan pesan sukses untuk admin
            modeladmin.message_user(request, f"Suggestion '{suggestion.name}' has been approved and published.", 'success')

        except Exception as e:
            # Jika ada error, tampilkan pesan error
            modeladmin.message_user(request, f"Failed to approve '{suggestion.name}': {e}", 'error')


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    """Konfigurasi tampilan admin untuk model Suggestion."""
    list_display = ('name', 'status', 'regency', 'created_at')
    list_filter = ('status', 'regency')
    search_fields = ('name', 'descriptions', 'regency')
    readonly_fields = ('created_at',)
    inlines = [SuggestionPhotoInline]
    actions = [approve_suggestion]

    fieldsets = (
        ('Suggestion Details', {
            'fields': ('name', 'status', 'category', 'descriptions')
        }),
        ('Location Info', {
            'fields': ('street', 'sub_district', 'regency', ('latitude', 'longitude'))
        }),
        ('Contact & Price', {
            'fields': ('phone_number', 'email', ('entrance_ticket_min', 'entrance_ticket_max'))
        }),
        ('Facilities', {
            'fields': ('facilities',)
        }),
    )
    filter_horizontal = ('facilities',) # Tampilan lebih baik untuk ManyToManyField