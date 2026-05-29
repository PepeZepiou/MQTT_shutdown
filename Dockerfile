FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m app

COPY client/config/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app client/ ./

USER app

CMD ["python", "app/mqtt_client.py"]
