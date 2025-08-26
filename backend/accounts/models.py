from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Roles para permisos
    ROLE_CHOICES = (
        ('user', 'User'),
        ('profesor', 'Profesor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    # Campos esenciales para login y contacto
    email = models.EmailField(unique=True)  # obligatorio y único

    # Campo para borrado lógico
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        """Borrado lógico en lugar de físico"""
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"ID: {self.id} | Usuario: {self.first_name} {self.last_name} | Email: {self.email} | Rol: {self.role}"
