from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(8, message="Debe tener al menos 8 caracteres"),
            MaxLengthValidator(20, message="No puede tener más de 20 caracteres")
        ]
    )
    first_name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(3, message="Debe tener al menos 3 caracteres"),
            MaxLengthValidator(20, message="No puede tener más de 20 caracteres")
        ]
    )
    last_name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(3, message="Debe tener al menos 3 caracteres"),
            MaxLengthValidator(20, message="No puede tener más de 20 caracteres")
        ]
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "No puede estar vacío.",
            "invalid": "Debe ser un correo electrónico válido."
        }
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password', 'password2')

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Debe contener al menos una letra mayúscula")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Debe contener al menos un número")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
