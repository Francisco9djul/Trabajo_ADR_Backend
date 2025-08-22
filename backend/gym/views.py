from django.shortcuts import render
from rest_framework import viewsets
from .models import Ejercicio, Bloque, BloqueEjercicio, Rutina, Formulario, Notificacion, UsuarioNotificacion
from .serializers import (
    EjercicioSerializer, BloqueSerializer, BloqueEjercicioSerializer,
    RutinaSerializer, FormularioSerializer, NotificacionSerializer,
    UsuarioNotificacionSerializer
)

# Create your views here.

# Ejercicio
class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

# BloqueEjercicio 
class BloqueEjercicioViewSet(viewsets.ModelViewSet):
    queryset = BloqueEjercicio.objects.all()
    serializer_class = BloqueEjercicioSerializer

# Bloque
class BloqueViewSet(viewsets.ModelViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer

# Rutina
class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer

# Formulario
class FormularioViewSet(viewsets.ModelViewSet):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer

# Notificacion
class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

# UsuarioNotificacion
class UsuarioNotificacionViewSet(viewsets.ModelViewSet):
    queryset = UsuarioNotificacion.objects.all()
    serializer_class = UsuarioNotificacionSerializer