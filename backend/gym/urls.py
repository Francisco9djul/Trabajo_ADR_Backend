from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    EjercicioViewSet, BloqueViewSet, BloqueEjercicioViewSet,
    RutinaViewSet, FormularioViewSet, NotificacionViewSet,
    UsuarioNotificacionViewSet
)

router = DefaultRouter()
router.register(r'ejercicios', EjercicioViewSet)
router.register(r'bloques', BloqueViewSet)
router.register(r'bloques-ejercicios', BloqueEjercicioViewSet)
router.register(r'rutinas', RutinaViewSet)
router.register(r'formularios', FormularioViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'usuario-notificaciones', UsuarioNotificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
