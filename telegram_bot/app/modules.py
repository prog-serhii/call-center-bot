from telebot import types
import requests
from config import URL_GET


class Keyboard:
    @staticmethod
    def first_keyboard():
        first_keyboard = types.ReplyKeyboardMarkup(True)
        timing_button = types.KeyboardButton(text='Рабочее время ' + u'\U000023F3')
        call_back_button = types.KeyboardButton(text='Передзвонить ' + u'\U0001F4DE')
        first_keyboard.add(timing_button, call_back_button)

        return first_keyboard

    @staticmethod
    def link_keyboard():
        first_keyboard_link = types.InlineKeyboardMarkup()
        button_site = types.InlineKeyboardButton(text='Наш сайт', url='https://habrahabr.ru')
        first_keyboard_link.add(button_site)

        return first_keyboard_link

    @staticmethod
    def phone_keyboard():
        phone_keyboard = types.InlineKeyboardMarkup()
        correct_button = types.InlineKeyboardButton(text='Да ' + u'\U00002705', callback_data='correct')
        change_button = types.InlineKeyboardButton(text='Изменить ' + u'\U0001F6AB', callback_data='change')
        phone_keyboard.add(correct_button, change_button)

        return phone_keyboard

    @staticmethod
    def call_keyboard():
        call_keyboard = types.InlineKeyboardMarkup()
        new_call_button = types.InlineKeyboardButton(text='Передзвонить ' + u'\U0001F4DE', callback_data='new_call')
        call_keyboard.add(new_call_button)

        return call_keyboard


class Actions:
    def __init__(self, bot_name, db_name, users_table):
        self.bot = bot_name
        self.db = db_name
        self.UsersTable = users_table

    def get_request(self, message):
        pass
        r = requests.get(
            URL_GET,
            params={
                'user_name': message.chat.username,
                'user_phone': self.UsersTable.query.filter_by(telegram_name=message.chat.username).first().phone
            }
        )
        print(r)
        # print(message.chat.username)
        # print(self.UsersTable.query.filter_by(telegram_name=message.chat.username).first().phone)

    def send_welcome(self, message):
        self.bot.send_message(
            message.chat.id,
            "Здраствуй наш новый друг " + u'\U0001F603' + '!',
            reply_markup=Keyboard.first_keyboard()
            )

    def send_call_back(self, message):
        self.bot.send_message(
            message.chat.id,
            'Вам скоро перезвонят.',
            reply_markup=Keyboard.first_keyboard()
        )

    def send_input_phone(self, message):
        self.bot.send_message(
            message.chat.id,
            'Пожалуйста, введите ваш номер:'
        )

    def send_phone_saved(self, message):
        self.bot.send_message(
            message.chat.id,
            'Ваш номер телефона сохранен.',
            reply_markup=Keyboard.call_keyboard()
        )

    def send_timing(self, message):
        self.bot.send_message(
            message.chat.id,
            'Мы работаем сегодня.',
            reply_markup=Keyboard.link_keyboard()
        )

    def send_ask_phone(self, message, user):
        self.bot.send_message(
            message.chat.id,
            "Это Ваш номер телефона?"
        )
        self.bot.send_message(
            message.chat.id,
            f'{user.phone}',
            reply_markup=Keyboard.phone_keyboard()
        )

    def request_call_back(self, message):
        user = self.UsersTable.query.filter_by(telegram_name=message.chat.username).first()
        # если у пользователя есть номер телефона в БД
        if user.phone:
            self.send_ask_phone(message, user)
        else:
            self.send_input_phone(message)

    def new_user(self, message):
        # проверка по telegram id - не работает
        #user = self.UsersTable.query.filter_by(telegram_id=message.chat.id).first()

        user = self.UsersTable.query.filter_by(telegram_name=message.chat.username).first()
        # если нету пользователя
        if not user:
            # то создаем
            user = self.UsersTable(
                telegram_name=message.chat.username,
                telegram_id=message.from_user.id,
                name=str(message.chat.first_name) + ' ' + str(message.chat.last_name)
            )
            # сохраняем изменения
            self.db.session.add(user)
            self.db.session.commit()

    def save_change_phone(self, message, phone_of_user):
        # поиск пользователя в БД
        user = self.UsersTable.query.filter_by(telegram_name=message.chat.username).first()
        # изменение номера
        user.phone = phone_of_user
        # сохраняем изменения
        self.db.session.add(user)
        self.db.session.commit()


class Statistic:
    def __init__(self, db_name, users_table, messages_table):
        self.db = db_name
        self.UsersTable = users_table
        self.MessagesTable = messages_table
        self.id = 0

    def find_user_id(self, user):
        user_id = self.UsersTable.query.filter_by(telegram_name=user).first()
        user_id = int(user_id.id)
        return user_id

    def command(self, user, text):
        # Начало работы пользователя с ботом или команда / start
        self.id = 1
        id_user = self.find_user_id(user)
        act_for_stat = self.MessagesTable(id_user=id_user, id_action=self.id, message=text)
        self.db.session.add(act_for_stat)
        self.db.session.commit()

    def inline_key(self, user, text):
        # Нажатие на инлайн кнопку
        self.id = 2
        id_user = self.find_user_id(user)
        act_for_stat = self.MessagesTable(id_user=id_user, id_action=self.id, message=text)
        self.db.session.add(act_for_stat)
        self.db.session.commit()

    def reply_key(self, user, text):
        # Нажатие на кнопку под клавиатурой
        self.id = 3
        id_user = self.find_user_id(user)
        act_for_stat = self.MessagesTable(id_user=id_user, id_action=self.id, message=text)
        self.db.session.add(act_for_stat)
        self.db.session.commit()

    def phone_number(self, user, text):
        # Отправка номера телефона
        self.id = 4
        id_user = self.find_user_id(user)
        act_for_stat = self.MessagesTable(id_user=id_user, id_action=self.id, message=text)
        self.db.session.add(act_for_stat)
        self.db.session.commit()

    def message(self, user, text):
        # Отправка обычного сообщение
        self.id = 5
        id_user = self.find_user_id(user)
        act_for_stat = self.MessagesTable(id_user=id_user, id_action=self.id, message=text)
        self.db.session.add(act_for_stat)
        self.db.session.commit()
