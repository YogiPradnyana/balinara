# apps/suggestions/views.py
from rest_framework import viewsets, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Suggestion
from .serializers import SuggestionSerializer

# Kita hanya gunakan mixin untuk 'create' dan 'list' (opsional)
class SuggestionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint untuk user mengirimkan suggestion tempat baru.
    Hanya mengizinkan method POST (create).
    """
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.AllowAny] # Siapapun boleh mengirim suggestion