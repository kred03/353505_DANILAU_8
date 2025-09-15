@echo off
echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Проверка проекта...
python manage.py check

echo Применение миграций...
python manage.py migrate

echo Создание суперпользователя (если нужно)...
echo Если суперпользователь уже существует, нажмите Ctrl+C для отмены
python manage.py createsuperuser

echo Запуск сервера разработки...
python manage.py runserver

pause

