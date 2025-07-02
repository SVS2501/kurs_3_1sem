import psycopg
from app import app
from app import login_manager
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(id): # авторизация пользователя
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        if id[0:4] == '_CO_': # ID тренера начинается с _CO_
            username, password, role = cur.execute('SELECT username, passwd, rol '
                                            'FROM "coach" '
                                            'WHERE username = %s', (id[4:],)).fetchone()
        else: 
            username, password, role = cur.execute('SELECT username, passwd, rol '
                                            'FROM "athlete" '
                                            'WHERE username = %s', (id,)).fetchone()
    return User(id, username, password, role)