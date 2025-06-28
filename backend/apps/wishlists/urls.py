# backend/apps/wishlists/urls.py
from django.urls import path
from .views import WishlistListCreateView, WishlistDestroyView

urlpatterns = [
    path('', WishlistListCreateView.as_view(), name='wishlist-list-create'),
    path('destinations/<int:destination_id>/',
         WishlistDestroyView.as_view(), name='wishlist-destroy'),
]
