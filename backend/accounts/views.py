from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_deleted=False)  #  Solo usuarios activos
    serializer_class = CustomUserSerializer

    def perform_destroy(self, instance):
        """Sobreescribir borrado físico por lógico"""
        instance.delete()
