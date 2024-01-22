# Проект REST API для Меню Ресторана с FastAPI и PostgreSQL

## Проект представляет собой реализацию REST API для управления меню ресторана
с использованием FastAPI и базы данных PostgreSQL.
В качестве ORM использовался SQLAlchemy, для миграций использовался Alembic.

### Основные функции:
+ CRUD операции: Поддерживает все основные операции для работы с данными.
+ Структура данных: Включает три основных сущности - Меню, Подменю и Блюдо, со строгими зависимостями и условиями.
+ Управление данными: Организация и контроль за связями между меню, подменю и блюдами.
+ Автоматическое управление связанными данными: Автоматическое удаление подменю и блюд при удалении меню, а также блюд при удалении подменю.
+ Форматирование цен: Цены блюд представлены с округлением до двух знаков после запятой.
+ Агрегированная информация: Включает количество подменю и блюд в списке меню, а также количество блюд в списке подменю.

### Запуск и использование
Для запуска проекта необходимо:
+ Клонировать данный проект из репозитория
+ Создать и активировать виртуальное окружение (предпочтительно __venv__)
+ Установить зависимости из файла __requirements.txt__ ```pip install -r requirements.txt```
+ Создать базу данных с предпочитаемым названием
+ Создать в корне проекта файл __.env__ и внести в него параметры базы данных (пример оформления файла в __.env.sample__
+ Применить миграции при помощи команды ```alembic upgrade head```
+ Запустить сервер командой ```uvicorn app.main:app --reload```

После выполнения перечисленных пунктов можно начать работать с API.
