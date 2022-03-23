![Run server](https://github.com/leonholly/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## YaMDB
### Описание:

Проект **YaMDB** собирает отзывы пользователей на различные произведения 
(музыка, фильмы, книги и т.п.) и позволяет поставить каждому произведению оценку. 
По этим оценкам для каждого произведения формируется рейтинг. Произведения разделяются на категории, 
каждое произведение можно отнести к одному или нескольким жанрам. Под отзывами 
пользователей можно оставлять комментарии. Проект не имеет графического интерфейса и доступен
только как API-сервис.

### Технологии:

Django,
Gunicorn,
Nginx,
Docker.

### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:leonholly/infra_sp2.git
```

```
cd infra_sp2/infra
```

Собрать и запустить Docker-контейнер:

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Перенести статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

### Примеры запросов:

#### http://localhost/api/v1/titles/

Этот запрос вернёт список всех произведений, которые есть в базе данных.

#### http://localhost/api/v1/titles/?year=2009

Такой запрос вернёт только произведения, появившиеся в 2009 году.

#### http://localhost/api/v1/titles/1/reviews/

Такой запрос вернёт список всех отзывов пользователей на произведение с 
уникальным идентификатором = 1.

#### http://localhost/api/v1/titles/1/reviews/1/comments/

Такой запрос вернёт список всех комментариев пользователей на отзыв с 
уникальным идентификатором = 1 на произведение с 
уникальным идентификатором = 1.

#### http://lemonetch.ddns.net/redoc/

Перейдите по этой ссылке, если хотите посмотреть все доступные запросы к API

### Авторы:

leonholly, 
Pablo9860,
Fizik05