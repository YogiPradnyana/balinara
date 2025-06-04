"""
URL configuration for gemini_chatbot_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# gemini_chatbot_project/urls.py

from django.contrib import admin
from django.urls import path, include # Pastikan include diimpor

urlpatterns = [
    path('admin/', admin.site.urls),
    # UBAH MENJADI INI UNTUK MENAMBAHKAN PREFIX 'api/'
    path('api/', include('chat.urls')), # <--- BARIS YANG BENAR
    # Jika Anda ingin ada sesuatu di root URL ('/'), Anda bisa menambahkan rute lain di sini
    # Misalnya, untuk redirect ke /api/messages/ seperti yang kita diskusikan sebelumnya:
    # from chat.views import api_root_redirect
    # path('', api_root_redirect),
]