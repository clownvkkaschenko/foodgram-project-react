<div id="header" align="center">
  <h1>Foodgram Project</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-brightgreen"/>
  <img src="https://img.shields.io/badge/Django-3.2.16-blueviolet"/>
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.2.14-orange"/>
  <img src="https://img.shields.io/badge/Postgres-yellow"/>
  <img src="https://img.shields.io/badge/Docker-red"/>
  <img src="https://img.shields.io/badge/Nginx-blue"/>
  <img src="https://img.shields.io/badge/YandexCloud-gray"/>
</div>

<img src="https://github.com/clownvkkaschenko/FoodgramProject/actions/workflows/main.yml/badge.svg"/>

Проект Foodgram позволяет пользователям публиковать свои рецепты, подписываться на других авторов и добавлять рецепты в избранное или список покупок.

**Backend разрабатывал Иван Конышкин**

**Frontend разрабатывал Yandex.Практикум**
# Запуск проекта:
- Клонируйте репозиторий и перейдите в него
  ```
  git clone git@github.com:clownvkkaschenko/FoodgramProject.git
  ```
- Cоздайте файл .env в папке **infra** и заполните этот файл данными представленными ниже
  ```
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=postgres
  POSTGRES_USER=postgres
  DB_HOST=db
  DB_PORT=5432
  POSTGRES_PASSWORD=password
  ```
- Из папки **infra** и запустите docker-compose 
  ```
  ~$ docker-compose up -d --build
  ```
- В контейнере web выполните миграции, создайте суперпользователя и соберите статику
  ```
  ~$ docker-compose exec web python manage.py makemigrations
  ~$ docker-compose exec web python manage.py migrate
  ~$ docker-compose exec web python manage.py createsuperuser
  ~$ docker-compose exec web python manage.py collectstatic --no-input
  ```
- Загрузите подготовленые данные из fixture.json в БД
  ```
  ~$ docker-compose exec web python manage.py loaddata db.json
  ```
После этого проект будет доступен по url-адресу **127.0.0.1**

Документация к API доступна по url-адресу **127.0.0.1/api/docs/**
