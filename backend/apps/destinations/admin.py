# apps/destinations/admin.py
from django.contrib import admin
from .models import Destination, DestinationImage


class DestinationImageInline(admin.TabularInline):  # Atau admin.StackedInline
    model = DestinationImage
    extra = 1  # Jumlah form kosong untuk upload gambar baru
    fields = ('image', 'alt_text', 'is_primary')
    # readonly_fields = ('uploaded_at',) # Jika ingin menampilkan tapi tidak bisa diedit


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'average_rating',
                    'total_reviews', 'is_published', 'updated_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('name', 'description',
                     'address__street', 'address__regency')
    # Otomatis isi slug berdasarkan nama
    prepopulated_fields = {'slug': ('name',)}
    # Menampilkan form DestinationImage langsung di halaman edit Destination
    inlines = [DestinationImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'is_published')
        }),
        ('Details', {
            'fields': ('category', 'address', 'contact', 'ticket_price_range', 'operational_hours')
        }),
        ('Ratings & Reviews (Read-only)', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)  # Bisa diciutkan
        }),
        ('Facilities', {
            'fields': ('facilities',),
            'classes': ('collapse',)
        }),
        # ('Timestamps (Read-only)', {
        #     'fields': ('created_at', 'updated_at'),
        #     'classes': ('collapse',)
        # }),
    )
    # Untuk ManyToManyField 'facilities', Django Admin menyediakan widget yang baik secara default.
    # Anda bisa mengkustomisasinya lebih lanjut dengan filter_horizontal atau filter_vertical jika daftarnya panjang.
    filter_horizontal = ('facilities',)  # atau filter_vertical

# Anda juga bisa mendaftarkan DestinationImage secara terpisah jika ingin mengelolanya dari menu sendiri
# @admin.register(DestinationImage)
# class DestinationImageAdmin(admin.ModelAdmin):
#     list_display = ('destination', 'alt_text', 'is_primary', 'uploaded_at')
#     list_filter = ('destination', 'is_primary')
#     search_fields = ('alt_text', 'destination__name')
