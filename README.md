Проект представляет из себя REST API модуль к социальной сети YaMDb. 
Позволяет через различные приложения, http запросы просматривать отзывы на произведения разных категорий и жанров, коментарии к ним и их рейтинг внутри проекта.
Проект YaMDb не содержит самих произведений.
Так же авторизованным пользователям предоставляется возможность оставлять отзывы коментарии к произведениям и указывать свою оценку, а так же удалять и изменять свой контент.
Получение доступа по токену реализовано чрезе библиотеку default_token_generator.

### Как запустить проект:

1) Клонировать репозиторий и перейти в него в командной строке.
Находясь в корневой папке проекта ввести в терминале(Bash) команду
```
git clone git@github.com:freemirror/api_yamdb.git
```
2) Вводим пароль и переходим в появившуюся папку с проектом, введя команду.
```
cd api_yamdb
```

3)Cоздать и активировать виртуальное окружение/
Вводим в терминал поочередно команды.

```
python -m venv venv
```

```
source venv/Scripts/activate
```
4) Далее обновляем программу pip (загрузчик внешних библиотек)
```
Вводим в терминал команду.
python3 -m pip install --upgrade pip
```

5)Установить зависимости из файла requirements.txt:
Вводим в терминал команду.
```
pip install -r requirements.txt
```

6) Выполняем миграции:
Вводим в терминал команду.
```
python3 manage.py migrate
```

7) Запустить проект:

```
python3 manage.py runserver
```

Примеры запросов к API:
GET http://127.0.0.1:8000/api/v1/titles/
GET http://127.0.0.1:8000/api/v1/titles/88/reviews/

POST http://127.0.0.1:8000/api/v1/titles/89/reviews/74/comments/
Content-Type: application/json
Authorization: Bearer {token}

{
    "title_id": 89,
    "review_id": 74,
    "text": "Полностью согласен с отзывом."
}
