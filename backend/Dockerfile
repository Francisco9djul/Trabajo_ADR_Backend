# Imagen base
FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema (para psycopg2 y compilación)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Variables de entorno por defecto (se pueden sobreescribir con docker run o docker-compose)
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=gym_api.settings

# Recoger archivos estáticos (si usás el admin de Django o media)
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Para desarrollo: runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Para producción, conviene:
# CMD ["gunicorn", "gym_api.wsgi:application", "--bind", "0.0.0.0:8000"]
