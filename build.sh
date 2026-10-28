#!/usr/bin/env bash

# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Сборка стилей (WhiteNoise)
python manage.py collectstatic --noinput

# 3. Применение миграций (создание таблиц в PostgreSQL)
python manage.py migrate

# 4. Загрузка данных из data.json (рецепты, категории)
python manage.py loaddata data.json

# 5. Создание суперпользователя (админа), если его еще нет
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')"

# 6. Очистка всех пользователей, КРОМЕ админа (чтобы регистрация не выдавала ошибку "занято")
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.exclude(username='admin').delete()"