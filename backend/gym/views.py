from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Ejercicio, Bloque, BloqueEjercicio, Rutina, Formulario, Notificacion, UsuarioNotificacion
from .serializers import (
    EjercicioSerializer, BloqueSerializer, BloqueEjercicioSerializer,
    RutinaSerializer, FormularioSerializer, NotificacionSerializer,
    UsuarioNotificacionSerializer
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsAuthenticated]  # Solo para usuarios logueados 

# BloqueEjercicio 
class BloqueEjercicioViewSet(SoftDeleteViewSet):
    queryset = BloqueEjercicio.objects.all()
    serializer_class = BloqueEjercicioSerializer
    permission_classes = [IsAuthenticated]  

# Bloque
class BloqueViewSet(SoftDeleteViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer
    permission_classes = [IsAuthenticated]  

class RutinaViewSet(SoftDeleteViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'profesor':
            return Rutina.objects.all()  # profesores pueden ver todas
        return Rutina.objects.filter(usuario=user)  # alumnos solo las suyas

    def perform_create(self, serializer):
        user = self.request.user

        # Profesores pueden crear rutinas pero **no para sí mismos**
        if user.role == 'profesor':
            usuario_destino = serializer.validated_data.get('usuario')
            if usuario_destino == user:
                raise PermissionDenied("No podés crear una rutina para vos mismo.")
        else:
            # alumnos/otros roles no pueden crear rutinas
            raise PermissionDenied("Solo los profesores pueden crear rutinas.")

        serializer.save()  # se guarda con el usuario indicado en el JSON

# Formulario
class FormularioViewSet(SoftDeleteViewSet):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    permission_classes = [IsAuthenticated]  

# Notificacion
class NotificacionViewSet(SoftDeleteViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]  

# UsuarioNotificacion
class UsuarioNotificacionViewSet(SoftDeleteViewSet):
    queryset = UsuarioNotificacion.objects.all()
    serializer_class = UsuarioNotificacionSerializer
    permission_classes = [IsAuthenticated]   