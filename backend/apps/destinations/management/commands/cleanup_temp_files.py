# apps/destinations/management/commands/cleanup_temp_files.py

import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.destinations.models import TemporaryImage


class Command(BaseCommand):
    help = 'Deletes temporary images older than 24 hours.'

    def handle(self, *args, **options):
        # Tentukan batas waktu, misalnya file yang lebih tua dari 24 jam
        time_threshold = timezone.now() - datetime.timedelta(hours=24)

        # Cari semua objek TemporaryImage yang lebih tua dari batas waktu
        old_temp_images = TemporaryImage.objects.filter(
            uploaded_at__lt=time_threshold)

        # Hitung jumlahnya untuk laporan
        count = old_temp_images.count()

        if count > 0:
            # Hapus satu per satu untuk memastikan metode .delete() kustom di model terpanggil
            # dan file fisiknya ikut terhapus.
            for temp_image in old_temp_images:
                temp_image.delete()

            # Tampilkan pesan sukses di konsol
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted {count} old temporary image(s).'))
        else:
            self.stdout.write(self.style.SUCCESS(
                'No old temporary images to delete.'))
