FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn psycopg2-binary

COPY . .

RUN SECRET_KEY=build-dummy-key python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "medmaster.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]