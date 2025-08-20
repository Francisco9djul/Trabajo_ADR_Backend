from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # campos que se muestran en la lista
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser")

    # Para mostrar el campo "role" en la edición
    fieldsets = UserAdmin.fieldsets + (
        ("Rol personalizado", {"fields": ("role",)}),
    )

    # Para incluir "role" también en la creación de usuario desde admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rol personalizado", {"fields": ("role",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)