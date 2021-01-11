import os

# токен замените на свой
TOKEN = '1122081078:AAEqMylSD5XrmU2QfoWWxLpIxQW93PKR2qs'
URL = "https://serhiikazmiruk.pythonanywhere.com/"
URL_GET = "http://178.124.155.166:34055/bot"

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
	DEBUG = False

    # SQLite 
	#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_base.sqlite')
	
	# MySQL
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://SerhiiKazmiruk:password123.@SerhiiKazmiruk.mysql.pythonanywhere-services.com/SerhiiKazmiruk$database'
	# SerhiiKazmiruk - имя пользователя БД
	# password123. - парольпользователя БД
	# SerhiiKazmiruk.mysql.pythonanywhere-services.com/ - сервер где есть БД
	# SerhiiKazmiruk$database - назва БД
	
	SQLALCHEMY_TRACK_MODIFICATIONS = False


