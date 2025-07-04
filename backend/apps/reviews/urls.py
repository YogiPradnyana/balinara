from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reviews_api'

# Membuat router dan mendaftarkan ViewSet kita dengannya.
router = DefaultRouter()
router.register(r'temp-images', views.TemporaryReviewImageViewSet,
                basename='temp-review-image')
router.register(r'', views.ReviewViewSet,
                basename='reviews')

# URL API akan ditentukan secara otomatis oleh router.
urlpatterns = [
    path('', include(router.urls)),
]
