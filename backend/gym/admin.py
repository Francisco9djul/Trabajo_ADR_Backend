from django.contrib import admin
from django.contrib import admin
from .models import Ejercicio, Bloque, BloqueEjercicio, Rutina, Formulario, Notificacion, UsuarioNotificacion

# Register your models here.

admin.site.register(Ejercicio)
admin.site.register(Bloque)
admin.site.register(BloqueEjercicio)
admin.site.register(Rutina)
admin.site.register(Formulario)
admin.site.register(Notificacion)
admin.site.register(UsuarioNotificacion)