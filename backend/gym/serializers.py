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
    ejercicioId = serializers.PrimaryKeyRelatedField(
        queryset=Ejercicio.objects.all(), source='ejercicio', write_only=True
    )

    class Meta:
        model = BloqueEjercicio
        fields = ['id', 'series', 'repeticiones', 'ejercicio', 'ejercicioId']

# Bloque
class BloqueSerializer(serializers.ModelSerializer):
    bloque_ejercicios = BloqueEjercicioSerializer(many=True)

    class Meta:
        model = Bloque
        fields = ['id', 'nombre', 'dia', 'bloque_ejercicios']

# Rutina
class RutinaSerializer(serializers.ModelSerializer):
    # Para recibir bloques en POST
    bloques = BloqueSerializer(many=True, write_only=True, required=False)
    # Para mostrar bloques al hacer GET
    bloques_read = BloqueSerializer(many=True, read_only=True, source='bloques')

    class Meta:
        model = Rutina
        fields = ['id', 'nombre', 'objetivo', 'usuario', 'bloques', 'bloques_read']

    def create(self, validated_data):
        bloques_data = validated_data.pop('bloques', [])
        user = self.context['request'].user

        # Solo profesores pueden crear rutinas
        if user.role != 'profesor':
            raise serializers.ValidationError("Solo los profesores pueden crear rutinas.")

        # Chequear que no se creen rutinas para sí mismos
        usuario_destino = validated_data.get('usuario')
        if usuario_destino == user:
            raise serializers.ValidationError("No podés crear una rutina para vos mismo.")

        # Crear rutina
        rutina = Rutina.objects.create(**validated_data)

        # Crear bloques y ejercicios asociados
        for bloque_data in bloques_data:
            ejercicios_data = bloque_data.pop('bloque_ejercicios', [])
            bloque = Bloque.objects.create(rutina=rutina, **bloque_data)
            for e_data in ejercicios_data:
                BloqueEjercicio.objects.create(
                    bloque=bloque,
                    ejercicio=e_data['ejercicio'],  # usar _id si es FK
                    series=e_data['series'],
                    repeticiones=e_data['repeticiones']
                )
        return rutina


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
