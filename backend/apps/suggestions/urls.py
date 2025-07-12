from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuggestionViewSet # Hanya impor SuggestionViewSet

router = DefaultRouter()
# Hanya daftarkan URL untuk suggestions
router.register(r'suggestions', SuggestionViewSet, basename='suggestion')

urlpatterns = [
    path('', include(router.urls)),
]