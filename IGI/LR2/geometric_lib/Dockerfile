# Указываем базовый образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . .

# Устанавливаем зависимости (если есть requirements.txt)
# RUN pip install -r requirements.txt

# Команда для запуска приложения
CMD ["python", "script.py"]