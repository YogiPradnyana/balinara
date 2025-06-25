# chat/storages.py

from cloudinary_storage.storage import MediaCloudinaryStorage


class ChatImageStorage(MediaCloudinaryStorage):
    """
    Storage kustom khusus untuk gambar yang di-upload di dalam chat.

    Saat ini, class ini tidak menambahkan atau mengubah perilaku apa pun dari
    MediaCloudinaryStorage. Namun, dengan membuatnya menjadi class terpisah, 
    ini memberi kita fleksibilitas untuk menambahkan logika kustom di masa depan
    dengan mudah tanpa harus mengubah kode di banyak tempat.

    Contohnya, jika nanti kita ingin semua gambar chat disimpan dalam sub-folder
    dinamis berdasarkan ID sesi, kita bisa menambahkannya di sini.
    """
    pass
