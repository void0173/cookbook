#!/usr/bin/env bash
# Установка зависимостей
pip install -r requirements.txt

# Сборка стилей (WhiteNoise)
python manage.py collectstatic --noinput

# Применение миграций (создание таблиц в PostgreSQL)
python manage.py migrate

# Загрузка данных из data.json (рецепты, категории)
python manage.py loaddata data.json

# Создание суперпользователя (админа), если его еще нет
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')"