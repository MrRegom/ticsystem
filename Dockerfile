# Usa la imagen oficial de Python 3.12 basada en Debian slim (ligera)
FROM python:3.12-slim

# Establece variables de entorno para optimizar Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema requeridas para compilar paquetes y manejar BD
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los requerimientos y los instala
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . /app/

# Crea carpeta de estáticos si no existe
RUN mkdir -p /app/staticfiles

# Expone el puerto donde correrá gunicorn (8000)
EXPOSE 8000

# Script de inicio (ejecuta migraciones, recolecta estáticos y levanta Gunicorn)
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
