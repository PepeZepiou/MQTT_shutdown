FROM python:3.12-slim

# Evite les .pyc inutiles + logs propres
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/local/app

# Installer dépendances (optimisé cache)
COPY client/config/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY client/ ./

# Sécurité
RUN useradd -m app
USER app

# Lancer l'app
CMD ["python", "./app/mqtt_client.py"]
