from app import app, db
from app.models import UsersPhones, Messages, ActionsTable
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

manager = Manager(app)


# эти переменные доступны внутри оболочки без явного импорта
def make_shell_context():
    return dict(app=app, db=db, UsersPhones=UsersPhones, Messages=Messages, ActionsTable=ActionsTable)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()