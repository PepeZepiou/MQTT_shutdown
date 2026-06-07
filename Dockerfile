FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

WORKDIR   /app

RUN useradd -m app

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY --chown=app:app . .

USER app

CMD ["python", "app/mqtt_client.py"]
