from django.db import models
from django.conf import settings 
from django.core.validators import MinValueValidator

# Base para soft delete
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    objects = SoftDeleteManager()  # Solo devuelve activos
    all_objects = models.Manager()  # Devuelve todos (incluyendo borrados)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Sobrescribimos delete para hacerlo lógico"""
        self.is_active = False
        self.save()

# Ejercicio
class Ejercicio(SoftDeleteModel):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
# Bloque
class Bloque(SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    dia = models.CharField(max_length=50)
    ejercicios = models.ManyToManyField("Ejercicio", through='BloqueEjercicio', related_name='bloques')
    rutina = models.ForeignKey("Rutina", on_delete=models.CASCADE, related_name="bloques")

    def __str__(self):
        if self.bloque_ejercicios.exists():
            ejercicios_str = ", ".join(
                [f"{be.ejercicio.nombre} ({be.series}x{be.repeticiones})" for be in self.bloque_ejercicios.all()]
            )
        else:
            ejercicios_str = "Sin ejercicios"
        return f"Bloque: {self.nombre}, Día: {self.dia}, Rutina: {self.rutina.nombre}, Ejercicios: [{ejercicios_str}]"
        
# Clase asociativa EjercicioBloque    
class BloqueEjercicio(SoftDeleteModel):
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, related_name="bloque_ejercicios")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name="ejercicios_en_bloques")
    series = models.PositiveIntegerField()
    repeticiones = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.ejercicio.nombre} en Bloque {self.bloque.nombre}: {self.series}x{self.repeticiones}"

# Rutina
class Rutina(SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=255)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rutinas')

    def __str__(self):
        bloques_str = ", ".join([bloque.nombre for bloque in self.bloques.all()])
        return f"Rutina: {self.nombre}, Objetivo: {self.objetivo}, Usuario: {self.usuario.username}, Bloques: [{bloques_str}]"

# Formulario
class Formulario(SoftDeleteModel):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='formularios')
    nombre = models.CharField(max_length=100)
    fechaCreacion = models.DateField(auto_now_add=True)
    sexo = models.CharField(max_length=10, choices=(('M','Masculino'), ('F','Femenino'), ('X', 'No definido')), blank=True, null=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    altura = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    alergias = models.CharField(max_length=255, blank=True)
    enfermedades = models.TextField(blank=True) 
    lesiones = models.TextField(blank=True)
    medicacion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Formulario de {self.usuario.username} - {self.nombre} - {self.fechaCreacion}"

# Notificacion
class Notificacion(SoftDeleteModel):
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fechaCreacion = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-fechaCreacion"]

    def __str__(self):
        return f"{self.titulo} - {self.fechaCreacion}"

# Clase asociativa UsuarioNotificacion
class UsuarioNotificacion(SoftDeleteModel):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario_notificaciones')
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, related_name='usuario_notificaciones')
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.notificacion.titulo} - {'Leida' if self.leida else 'No leida'}"
