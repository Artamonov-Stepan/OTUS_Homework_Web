#!/bin/sh

# Обработка аргументов командной строки
BROWSER="chrome"  # значение по умолчанию
CONCURRENCY=""    # по умолчанию без параллельного запуска

while [ $# -gt 0 ]; do
  case "$1" in
    --browser)
      BROWSER="$2"
      shift 2
      ;;
    --concurrency)
      CONCURRENCY="-n $2"
      shift 2
      ;;
    *)
      # Все остальные аргументы передаем в pytest
      break
      ;;
  esac
done

# Создаем директории для результатов
mkdir -p /usr/src/app/allure-results
mkdir -p /usr/src/app/screenshots
mkdir -p /usr/src/app/logs

# Запускаем pytest с переданными параметрами
exec pytest -v $CONCURRENCY --browser $BROWSER "$@"