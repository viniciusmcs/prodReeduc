FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy project files
COPY . /app/

# Collect static files
ENV DJANGO_SETTINGS_MODULE=reeduc.settings_prod
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Create media directories
RUN mkdir -p /app/media/cadastros /app/media/familiares

EXPOSE 8000

# Run migrations, create default admin, then start gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && python -c \"import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','reeduc.settings_prod'); import django; django.setup(); from core.default_admin import create_default_admin; create_default_admin()\" 2>/dev/null; gunicorn reeduc.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]
