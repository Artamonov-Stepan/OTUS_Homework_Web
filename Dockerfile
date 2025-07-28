FROM python:3.11-alpine

# Устанавливаем системные зависимости
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    firefox \
    geckodriver \
    xvfb \
    bash \
    curl \
    # Дополнительные библиотеки для работы браузеров
    libstdc++ \
    nss \
    freetype \
    harfbuzz \
    ttf-freefont \
    # Для сборки Python-пакетов
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    make

# Создаём рабочую директорию
WORKDIR /usr/src/app

# Копируем зависимости Python
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Устанавливаем права на entrypoint
RUN chmod +x autotest_entrypoint.sh

# Настройка окружения
ENV PYTHONPATH=/usr/src/app
ENV PYTHONUNBUFFERED=1
ENV BASE_URL=http://host.docker.internal:8081
ENV DISPLAY=:99
ENV PATH="/usr/lib/chromium:/usr/bin:${PATH}"

# Точка входа
ENTRYPOINT ["/bin/sh", "./autotest_entrypoint.sh"]