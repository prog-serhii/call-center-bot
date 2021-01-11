from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
import urllib3

import telebot

import config



#proxy_url = "http://proxy.server:3128"
#telebot.api._pools = {
#    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
#}
#telebot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

# создание экземпляра приложения Flask
app = Flask(__name__)
app.config.from_object('config.BaseConfig')

# инициализирует расширения
sslify = SSLify(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# создание экземпляра приложения Telebot
bot = telebot.TeleBot(config.TOKEN, threaded=False)

from . import views
