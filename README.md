# Habit Tracker API

Полноценный backend-сервис для отслеживания привычек и напоминаний, с возможностью рассылки через Telegram.

---

## Аутентификация

- Регистрация / авторизация через email (JWT).
- Доступ к привычкам строго по владельцу.
- Публичные привычки доступны всем для просмотра, но только в режиме read-only.

---

## Основной функционал

### Привычки

Формула привычки:
Я буду [действие] в [время] в [место]


#### Поля модели:
- `пользователь` — владелец привычки
- `место` — место выполнения
- `время` — время выполнения
- `действие` — описание действия
- `признак_приятной_привычки` — булево значение
- `связанная_привычка` — FK на приятную привычку (опционально)
- `вознаграждение` — текстовое описание (опционально)
- `периодичность` — количество дней (по умолчанию: 1)
- `время_на_выполнение` — в секундах (до 120 секунд)
- `признак_публичности` — доступна ли привычка всем

#### Валидация:
- Нельзя одновременно указать вознаграждение и связанную привычку
- Время на выполнение — не более 120 секунд
- Привычка должна выполняться хотя бы раз в 7 дней
- В связанные привычки можно указывать только приятные
- Приятная привычка не может иметь награды или связанной привычки

---

## Эндпоинты

- `POST /api/register/` — регистрация
- `POST /api/token/` — получение JWT
- `GET /api/habits/` — список привычек текущего пользователя (с пагинацией)
- `GET /api/habits/public/` — публичные привычки (только просмотр)
- `POST /api/habits/create/` — создание новой привычки
- `PATCH /api/habits/<id>/update/` — редактирование
- `DELETE /api/habits/<id>/delete/` — удаление

---

## Пагинация

- Используется `PageNumberPagination`
- Кол-во привычек на странице: **5**

---

## Telegram-интеграция

- Напоминания отправляются через Telegram в заданное время
- Используется `Telegram Bot API`
- Реализовано на фоне через `Celery + Redis`

---

## Технологии

- `Django` / `DRF`
- `djoser` / `SimpleJWT`
- `Celery + Redis`
- `Telegram Bot API`
- `drf-yasg` — Swagger документация
- `django-cors-headers` — настройка CORS

---

## Документация

- Swagger UI: [`/swagger/`](http://<IP-АДРЕС>/swagger/)
- ReDoc: [`/redoc/`](http://<IP-АДРЕС>/redoc/)

---

## Запуск проекта локально

```bash
# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Запуск Redis (если локально)
redis-server

# Запуск Celery
celery -A config worker -l info

# Запуск Django сервера
python manage.py runserver
```

---

🌐 Развёртывание на сервере (Ubuntu 22.04, gunicorn + nginx + PostgreSQL)

### 1. Установка зависимостей

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib git -y
```
## Развёртывание на сервере (Ubuntu 22.04, Gunicorn + Nginx + PostgreSQL)

### 2. Настройка базы данных

```bash
sudo -u postgres psql

CREATE DATABASE habitdb;
CREATE USER habituser WITH PASSWORD 'your_strong_password';
ALTER ROLE habituser SET client_encoding TO 'utf8';
ALTER ROLE habituser SET default_transaction_isolation TO 'read committed';
ALTER ROLE habituser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE habitdb TO habituser;
\q
```

### 3. Клонирование проекта и настройка виртуального окружения

```bash
cd /var/www/
git clone https://github.com/yourname/habit-tracker.git
cd habit-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте следующие переменные:

```env
DEBUG=False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=your_domain_or_ip

DB_NAME=habitdb
DB_USER=habituser
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Применение миграций и сборка статики

После настройки окружения необходимо применить миграции и собрать статику:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

⚠️ Убедитесь, что виртуальное окружение активировано перед выполнением команд.

### 6. Настройка Gunicorn

Для того чтобы приложение работало с Gunicorn, создайте файл сервиса для systemd:

```bash
sudo nano /etc/systemd/system/habit.service
```
```ini
[Unit]
Description=Habit Tracker Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/habit-tracker
ExecStart=/var/www/habit-tracker/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target

```

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start habit
sudo systemctl enable habit
```

### 7. Перезапуск Gunicorn

После настройки сервиса Gunicorn, необходимо перезапустить systemd и запустить сам сервис:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start habit
sudo systemctl enable habit
```

### 8. Настройка Nginx

Создайте конфигурационный файл для Nginx:

```bash
sudo nano /etc/nginx/sites-available/habit
```

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/habit-tracker;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```
Создайте символическую ссылку для активации конфигурации:

```bash
sudo ln -s /etc/nginx/sites-available/habit /etc/nginx/sites-enabled
```

Проверьте конфигурацию и перезапустите Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

Эти шаги настроят Nginx для проксирования запросов на Gunicorn-сервер, обеспечивая правильную 
работу вашего веб-приложения.

### 9. Настройка CORS

Убедитесь, что в файле `settings.py` вашего Django-проекта добавлены следующие строки для 
настройки CORS:

1. Добавьте приложение `corsheaders` в список установленных приложений,
2. Добавьте middleware для обработки CORS-запросов,
3. Укажите домены, с которых разрешено выполнение запросов (например, если ваш фронтенд 
работает на localhost:8000):

```python
INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # или ваш домен
]
```
### 10. Настройка Celery и Redis

1. Установите Redis на вашем сервере,
2. После установки Redis, убедитесь, что он работает корректно. Вы можете проверить статус с 
помощью команды,
3. Запустите Celery с помощью следующей команды(Это запустит Celery worker для обработки 
асинхронных задач, таких как отправка уведомлений через Telegram или другие задачи, 
которые требуют фоновой обработки.)
4. Для продакшн-среды рекомендуется настроить Celery для автоматического запуска с 
использованием Supervisor или создать systemd unit-файл для управления Celery.

```bash
sudo apt install redis -y
sudo systemctl enable redis
sudo systemctl start redis

celery -A config worker -l info

sudo nano /etc/systemd/system/celery.service
```

В конфиге укажите:
```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/habit-tracker
ExecStart=/var/www/habit-tracker/venv/bin/celery -A config worker --loglevel=info
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
```

После этого выполните команды для перезагрузки systemd и запуска сервиса:
```bash
sudo systemctl daemon-reload
sudo systemctl enable celery
sudo systemctl start celery
```

### 11. Документация Swagger

1. После развертывания проекта, вы можете получить доступ к автоматической документации API 
через Swagger и ReDoc.

2. Swagger UI доступен по следующему адресу:

```text
http://your_domain_or_ip/swagger/
```

3. Для доступа к ReDoc (альтернативный вид документации):
```text
http://your_domain_or_ip/redoc/
```

Документация генерируется автоматически с использованием пакета drf-yasg, 
который интегрируется с Django REST Framework (DRF). В ней содержатся все необходимые 
эндпоинты и примеры запросов/ответов для взаимодействия с вашим API.

### 12. CI/CD и деплой

1. Для автоматизации деплоя можно использовать GitHub Actions или другие CI/CD инструменты для автоматического развертывания при каждом обновлении репозитория.

2. Для ручного деплоя, выполните следующие шаги:

   1. Перейдите в каталог вашего проекта:
   
   ```bash
   cd /var/www/habit-tracker
    ```
   
Обновите репозиторий с последними изменениями:

```bash
git pull origin main
```

Активируйте виртуальное окружение:

```bash
source venv/bin/activate
```

Установите или обновите зависимости:

```bash
pip install -r requirements.txt
```

Примените миграции базы данных:
```bash
python manage.py migrate
```

Соберите статику:
```bash
python manage.py collectstatic --noinput
```

Перезапустите Nginx:

```bash
sudo systemctl restart nginx
```
Этот процесс можно автоматизировать с помощью CI/CD инструментов, таких как GitHub Actions, 
GitLab CI, Jenkins и других. Настроив CI/CD, вы можете автоматически развертывать изменения 
на сервере, что ускорит процесс доставки и обновления функционала.




