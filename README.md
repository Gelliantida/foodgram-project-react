# Foodgram

![Foodgram-project workflow](https://github.com/Gelliantida/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


### Описание
Сервис Foodgram - онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, для приготовления одного или нескольких выбранных блюд.

### Стек технологий:
- Python
- Django
- Django Rest Framework
- PosgreSQL
- Docker

## Запуск проекта локально
Клонировать репозиторий:
```
git clone https://github.com/Gelliantida/foodgram-project-react.git
```

Перейти в директорию с репозиторием. 
Создать и активировать виртуальное окружение, обновить pip и установить зависимости:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Шаблон env-файла
- DB_ENGINE=<django.db.backends.postgresql>
- DB_NAME=<имя базы данных postgres>
- POSTGRES_USER=<пользователь бд>
- POSTGRES_PASSWORD=<пароль>
- DB_HOST=<db>
- DB_PORT=<5432>
- SECRET_KEY=<<секретный ключ проекта django>

### Для запуска локально:
```
cd backend
python manage.py runserver
```

Создать базу данных:
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Заупстить сервер:
```
python manage.py runserver
```

Для запуска проекта с frontend:
```
cd infra
docker-compose up --build
```

## Для работы с удаленным сервером:
* Выполните вход на свой удаленный сервер
```
ssh <username>@<host>
```

* Установите docker и docker-compose на сервер
* Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    SECRET_KEY=<секретный ключ проекта django>
    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow состоит из четырех шагов:
     - Проверка кода на соответствие PEP8;
     - Сборка и публикация образа бекенда на DockerHub;
     - Автоматический деплой на удаленный сервер;
     - Отправка уведомления в телеграм-чат.  
  
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Проект будет доступен по вашему IP или доменному имени.

## Проект доступен
- Проект запущен и доступен по http://158.160.33.37/
- Админ панель http://158.160.33.37//admin
- Админ логин: admin
- Админ пароль: admin
