# apps/common/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'common_api'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'facilities', views.FacilityViewSet, basename='facility')

urlpatterns = [
    path('', include(router.urls)),
]
