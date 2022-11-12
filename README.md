# Flask-приложение с сервисом рекомендации блюд по отзывам пользователей

## Подготовка к запуску:
- Создание SQLite db для веб-приложения: python3 create_db.py
- Создание первого пользователя перед запуском: python3 create_admin.py

## Запуск веб-приложения:
- Для Windows: set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
- Для Unix/Mac: ./run_webapp.sh или
export FLASK_APP=webapp && export FLASK_ENV=development && export FLASK_DEBUG=1 && flask run

## Меню веб-приложения:
- Главная страница
- Логин
- Выход
- Рекомендация
- Поиск
- Создание рецепта

## Рекомендация блюд на основе Collaborative Filering
Наиболее популярный рецепт вычисляется по следующей формуле:

![Screenshot](img/CF_regression.png)

###### End
