from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Ejercicio, Bloque, BloqueEjercicio, Rutina, Formulario, Notificacion, UsuarioNotificacion
from .serializers import (
    EjercicioSerializer, BloqueSerializer, BloqueEjercicioSerializer,
    RutinaSerializer, FormularioSerializer, NotificacionSerializer,
    UsuarioNotificacionSerializer
)

class SoftDeleteViewSet(viewsets.ModelViewSet):
    """Base para que todos hagan soft delete"""
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # esto marca is_active=False
        return Response(status=status.HTTP_204_NO_CONTENT)

# Ejercicio
class EjercicioViewSet(SoftDeleteViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

# BloqueEjercicio 
class BloqueEjercicioViewSet(SoftDeleteViewSet):
    queryset = BloqueEjercicio.objects.all()
    serializer_class = BloqueEjercicioSerializer

# Bloque
class BloqueViewSet(SoftDeleteViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer

# Rutina
class RutinaViewSet(SoftDeleteViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'profesor':
            raise PermissionDenied("Los profesores no pueden crear rutinas.")
        serializer.save(usuario=user)

# Formulario
class FormularioViewSet(SoftDeleteViewSet):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer

# Notificacion
class NotificacionViewSet(SoftDeleteViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

# UsuarioNotificacion
class UsuarioNotificacionViewSet(SoftDeleteViewSet):
    queryset = UsuarioNotificacion.objects.all()
    serializer_class = UsuarioNotificacionSerializer