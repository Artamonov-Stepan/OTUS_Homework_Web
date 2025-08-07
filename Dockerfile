# Установка базового образа
FROM python:3.12-alpine

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей + Chromium
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    tzdata \
 && pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir allure-pytest

# Копирование кода
COPY . .

# Переменные окружения для Chromium
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver

# Создание папок
RUN mkdir -p screenshots logs

# Запуск тестов с параметрами по умолчанию для Docker
CMD ["pytest", "--remote", "--browser=chrome", "--enable-vnc", "--enable-video", "-v", "--alluredir=allure-results"]