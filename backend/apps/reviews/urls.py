from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reviews_api'

# Membuat router dan mendaftarkan ViewSet kita dengannya.
router = DefaultRouter()
router.register(r'', views.DestinationViewSet,
                basename='reviews')

# URL API akan ditentukan secara otomatis oleh router.
urlpatterns = [
    path('', include(router.urls)),
]
