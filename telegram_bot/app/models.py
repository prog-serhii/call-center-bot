from app import db
from datetime import datetime


class UsersPhones(db.Model):
    __tablename__ = 'TABLE_CLIENTS'
    # уникальной ключ клиента
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(1000), default='no_name')
    # не используется
    inc_number = db.Column(db.String(20))
    # telegram
    telegram_name = db.Column(db.String(30))
    # telegram -id
    telegram_id = db.Column(db.BigInteger)
    # номер телефона
    phone = db.Column(db.String(20), default='')

    # relationship
    messages = db.relationship('Messages', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.telegram_name}>'


class ActionsTable(db.Model):
    __tablename__ = 'TABLE_ACTIONS'
    # уникальной ключ действия
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # описание
    name = db.Column(db.String(1000))

    # relationship
    messages = db.relationship('Messages', backref='action', lazy='dynamic')

    def __repr__(self):
        return f'<Action {self.name[:20]}>'


class Messages(db.Model):
    __tablename__ = 'TABLE_MESSAGES'
    # уникальной ключ
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('TABLE_CLIENTS.id'))
    # id_user = db.Column(db.Integer)
    id_action = db.Column(db.Integer, db.ForeignKey('TABLE_ACTIONS.id'))
    #id_action = db.Column(db.Integer)
    message = db.Column(db.String(1000), default='no_message')
    time = db.Column(db.DateTime(), default=datetime.utcnow)
