# Foodgram Project «Продуктовый помощник»
![](https://github.com/clownvkkaschenko/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Описание проекта:
Проект Foodgram позволяет пользователям публиковать свои рецепты. Так же пользователи могут подписываться на других авторов, добавлять рецепты в избранное или список покупок.
Проект  доступен по адресу - http://130.193.40.135
Документация к API доступна по адресу - http://130.193.40.135/api/docs/
# Запуск проекта на локальном компьютере:
Клонируйте репозиторий и перейдите в корневую папку:
```
git@github.com:clownvkkaschenko/foodgram-project-react.git
```
Cоздайте файл .env в папке infra. Заполните этот файл, придумайте и введите пароль в последней строке:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
DB_HOST=db
DB_PORT=5432
POSTGRES_PASSWORD=password
```
На вашем компьютере измените IP адрес для запуска проекта на IP «127.0.0.1»:
```
В папке infra/nginx.conf(server_name)
В папке backend/foodgram/settings.py(ALLOWED_HOSTS)
```
Что-бы в контейнер не скачивались образы с неправильным IP адресом, поменяйте настройки файла docker-compose.yml в папке infra:
```
В образе web, вместо строки «image:» вставьте:
    build: 
      context: ../backend 
      dockerfile: Dockerfile
```
Перейдите в папку infra и запустите docker-compose:
```
~$ docker-compose up -d --build
```
Теперь в контейнере web нужно выполнить миграции, создать суперпользователя, собрать статику и загрузить ингредиенты в БД из подготовленного csv файла:
```
~$ docker-compose exec web python manage.py makemigrations
~$ docker-compose exec web python manage.py migrate
~$ docker-compose exec web python manage.py createsuperuser
~$ docker-compose exec web python manage.py collectstatic --no-input
~$ docker-compose exec web python manage.py load_csv
```
Теперь проект доступен по адресу: http://127.0.0.1
Документация API к проекту доступна по адресу: http://127.0.0.1/api/docs/
# Запуск проекта на сервере:
Войдите на свой удаленный сервер в облаке, установите docker и docker-compose:
```
~$ sudo apt install docker.io
~$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
~$ sudo chmod +x /usr/local/bin/docker-compose
```
На вашем компьютере измените IP-адрес, на котором работает проект, на IP-вашего сервера:
```
В папке infra/nginx.conf(server_name)
```
На вашем компьютере перейдите в папку infra и скопируйте файлы docker-compose.yml, nginx.conf и папку docs из вашего проекта на сервер:
```
scp docker-compose.yml <ваш_username>@<host>:/home/<ваш_username>/docker-compose.yml
scp nginx.conf <ваш_username>@<host>:/home/<ваш_username>/nginx.conf
scp -r docs/ <ваш_username>@<host>:/home/<ваш_username>/docs/
```
Создайте на сервере файл .env и заполните его данными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
DB_HOST=db
DB_PORT=5432
POSTGRES_PASSWORD=password
```
Запустите docker-compose:
```
~$ sudo docker-compose up -d --build
```
Измените IP-адрес в файле setting.py(ALLOWED_HOSTS), в контейнере web на IP-адрес вашего сервера:
```
~$ sudo docker exec -it <название_контейнера> bash
```
После чего нужно выполнить миграции, создать суперпользователя, собрать статику и загрузить ингредиенты в БД из подготовленного csv файла:
```
~$ sudo docker-compose exec web python manage.py makemigrations
~$ sudo docker-compose exec web python manage.py migrate
~$ sudo docker-compose exec web python manage.py createsuperuser
~$ sudo docker-compose exec web python manage.py collectstatic --no-input
~$ sudo docker-compose exec web python manage.py load_csv
```
Теперь проект будет работать на вашем IP адресе.
# GitHub Actions:
Для запуска инструкций workflow добавьте в Secrets GitHub Actions переменные окружения. 
```
DOCKER_USERNAME - ваш логин от DockerHub
DOCKER_PASSWORD - ваш пароль от DockerHub
HOST - IP-адрес сервера
USER - имя пользователя для подключения к серверу
SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу
PASSPHRASE - нужно заполнять только если при создании ssh-ключа вы использовали фразу-пароль
DB_ENGINE - django.db.backends.postgresql
DB_NAME - имя БД
POSTGRES_USER - имя пользователя
POSTGRES_PASSWORD - пароль для пользователя
DB_HOST - db
DB_PORT - 5432
TELEGRAM_TO - ваш ID
TELEGRAM_TOKEN - токен бота, который будет отправлять вам сообщение
```
После этого, при пуше проекта, GitHub будет автоматически:

- проверять код в папке backend по правилам pep8
- собирать и пушить образы фронтенда и бекенда в ваш DockerHub
- пулить эти же образы на ваш сервер
- создавать на сервере файл .env для запуска контейнера
- запускать контейнер
- при успешном завершении тестирования произойдёт отправка уведомления в Telegram о том, что процесс деплоя успешно завершился
# Стек технологий:
![python-version](https://img.shields.io/static/v1?label=Python&message=3.7.9&color=brightgreen) ![django-version](https://img.shields.io/static/v1?label=Django&message=3.2.16&color=brightgreen) ![DRF-version](https://img.shields.io/static/v1?label=DjangoRestFramework&message=3.14.0&color=brightgreen) ![postgres](https://img.shields.io/static/v1?label=&message=PostgreSQL&color=grey) ![nginx](https://img.shields.io/static/v1?label=&message=Nginx&color=grey) ![Docker](https://img.shields.io/static/v1?label=&message=Docker&color=grey) ![Yandex-cloud](https://img.shields.io/static/v1?label=&message=YandexCloud&color=grey) ![GitHubActions](https://img.shields.io/static/v1?label=&message=GitHubActions&color=grey)
# Авторы:
- Backend: Иван Конышкин
- Frontend: YandexPracticum