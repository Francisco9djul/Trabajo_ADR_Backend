from rest_framework import serializers
from .models import Ejercicio, Bloque, BloqueEjercicio, Rutina, Formulario, Notificacion, UsuarioNotificacion

# Ejercicio
class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id', 'nombre']

# BloqueEjercicio (asociativa)
class BloqueEjercicioSerializer(serializers.ModelSerializer):
    ejercicio = EjercicioSerializer(read_only=True)
    ejercicio_id = serializers.PrimaryKeyRelatedField(
        queryset=Ejercicio.objects.all(), source='ejercicio', write_only=True
    )

    class Meta:
        model = BloqueEjercicio
        fields = ['id', 'bloque', 'ejercicio', 'ejercicio_id', 'series', 'repeticiones']

# Bloque
class BloqueSerializer(serializers.ModelSerializer):
    bloque_ejercicios = BloqueEjercicioSerializer(many=True, read_only=True)

    class Meta:
        model = Bloque
        fields = ['id', 'nombre', 'dia', 'rutina', 'bloque_ejercicios']

# Rutina
class RutinaSerializer(serializers.ModelSerializer):
    bloques = BloqueSerializer(many=True, read_only=True)
    
    class Meta:
        model = Rutina
        fields = ['id', 'nombre', 'objetivo', 'usuario', 'bloques']

    def create(self, validated_data):
        user = self.context['request'].user  # obtenemos el usuario que hace la petición
        if user.role == 'profesor':
            raise serializers.ValidationError("Los profesores no pueden crear rutinas.")
        # Asignamos el usuario actual automáticamente 
        validated_data['usuario'] = user
        return super().create(validated_data)

# Formulario
class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = [
            'id', 'usuario', 'nombre', 'fechaCreacion', 'sexo', 'edad',
            'peso', 'altura', 'alergias', 'enfermedades', 'lesiones',
            'medicacion', 'observaciones'
        ]

# Notificacion
class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'titulo', 'mensaje', 'fechaCreacion']

# UsuarioNotificacion
class UsuarioNotificacionSerializer(serializers.ModelSerializer):
    notificacion = NotificacionSerializer(read_only=True)
    notificacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Notificacion.objects.all(), source='notificacion', write_only=True
    )

    class Meta:
        model = UsuarioNotificacion
        fields = ['id', 'usuario', 'notificacion', 'notificacion_id', 'leida']
