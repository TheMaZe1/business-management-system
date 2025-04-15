FROM python:3.11-slim

# Установка системных пакетов
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    apt-get clean

# Установка рабочей директории
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем код приложения
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .
COPY .env .

# Открываем порт
EXPOSE 8000

# Старт приложения
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000