# tests_backend

## Установка

Склонируйте репозиторий и перейдите в нужную директорию
```sh
$ git clone https://github.com/v4filippoff/tests_backend.git
$ cd tests_backend
```

Создайте виртуальное окружение для пакетов Python и активируйте его
```sh
$ python -m venv venv
$ source venv/bin/activate
```

Установите все зависимости
```sh
$ pip install -r requirements.txt
```

Создайте миграции для базы данных и примените их
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

Запустите локальный сервер
```sh
$ python manage.py runserver
```

Перейдите к `http://localhost:8000/`
