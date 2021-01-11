
структура папок должна выглядеть примерно так:
    
    README.txt
    requirements.txt
    venv/
    telegram_bot/
        config.py
        manage.py
        app/
            __init__.py
            database.py
            models.py
            modules.py
            utils.py
            views.py

1. Создание виртуальной окружения (в корене проекта)

    python3 -m venv env
    source env/bin/activate

2. Установка зависимостей

    pip3 install -r requirements.txt

3. Необходимо создать БД (если это MySQL или PostgreSQL)

4. Настроить сonfig.py
    * TOKEN - токен бота
    * URL - url сервера где бот (для вебхука)
    * URL_GET - url call-центра для запросов
    
    * если хотите использувать SQLite то только надо
    * 1. раскомментировать строку с ней
    * 2. закомментировать строку с БД MySQL
    
    * если ето MySQL то подставить свои данные (в сonfig.py так розписано что и как)

5. Настройка БД

    * переход в директорию с проектом
    сd telegram_bot
    
    *настройка
    
    python3 manage.py db init
    python3 manage.py db migrate
    python3 manage.py db upgrade
    python3 manage.py shell
    >>> act1 = ActionsTable(id=1, name='Начало работы пользователя с ботом или команда / start') 
    >>> act2 = ActionsTable(id=2, name='Нажатие на инлайн кнопку') 
    >>> act3 = ActionsTable(id=3, name='Нажатие на кнопку под клавиатурой') 
    >>> act4 = ActionsTable(id=4, name='Отправка номера телефона') 
    >>> act5 = ActionsTable(id=5, name='Отправка обычного сообщение') 
    >>> db.session.add_all([act1, act2, act3, act4, act5])
    >>> db.session.commit()
    >>> exit()


6. Запуск сервера (если ето локальной)
    python3 manage.py runserver
    

