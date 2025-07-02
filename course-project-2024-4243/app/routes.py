from flask import render_template
from app import app
import psycopg
@app.route('/') # главная страница
def index():
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к БД
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor() # вывод спортсменов и тренеров
        coaches = cur.execute('SELECT username, fio, gender, bodyweight, height, age, social_media, achievements FROM coach').fetchall()
        athletes = cur.execute('SELECT username, fio, gender, bodyweight, height, age, social_media FROM athlete').fetchall()
    return render_template('index.html',coaches = coaches, athletes = athletes) 

@app.route('/testdb') # проверка подключения к БД
def test_connection():
    con = None
    message = ""
    try:
        con = psycopg.connect(host=app.config['DB_SERVER'], # подключение к БД
                              user=app.config['DB_USER'],
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'])
    except Exception as e: # вывод результата проверки
        message = f"Ошибка подключения: {e}"
    else:
        message = "Подключение успешно"
    finally:
        if con:
            con.close()
        return message
    
@app.route('/excercises') # вывод всех упражнений и техники выполнения
def get_excercises():
    with psycopg.connect(host=app.config['DB_SERVER'],# подключение к БД
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        excercises = cur.execute(f'SELECT nazv, techniqe FROM exercise').fetchall()
    return render_template('excercises.html',excercises=excercises)

from flask import request

from app.forms import ATH_RegistrationForm
from flask import render_template

from werkzeug.security import generate_password_hash
from app import app
from flask import redirect, render_template, flash
from app.forms import ATH_RegistrationForm

@app.route('/AT_register', methods=['GET', 'POST']) # регистрация спортсмена
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = ATH_RegistrationForm()
    if reg_form.validate_on_submit(): 
        login = reg_form.username.data # получение данных из формы регистрации
        password_hash = generate_password_hash(reg_form.password.data)
        age = reg_form.age.data
        fio = reg_form.FIO.data
        height = reg_form.height.data
        weight = reg_form.weight.data
        media = reg_form.media.data
        gender = reg_form.gender.data
        with psycopg.connect(host=app.config['DB_SERVER'],# подключение к БД
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            cur.execute('INSERT INTO athlete (username, passwd,fio,gender,bodyweight,height,age,social_media)' # добавление нового пользователя в базу данных
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (login,password_hash,fio,gender,weight,height,age,media))
        # создание записи в таблице используя password_hash
        flash(f'Регистрация {reg_form.username.data} успешна', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация спортсмена', form=reg_form) # вывод страницы регистрации


from app.forms import CO_RegistrationForm

@app.route('/CO_register', methods=['GET', 'POST'])# регистрация тренера
def co_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = CO_RegistrationForm()  
    if reg_form.validate_on_submit():
        login = reg_form.username.data # получение данных из формы регистрации
        password_hash = generate_password_hash(reg_form.password.data)
        age = reg_form.age.data
        fio = reg_form.FIO.data
        height = reg_form.height.data
        weight = reg_form.weight.data
        media = reg_form.media.data
        achv = reg_form.achv.data
        gender = reg_form.gender.data
        with psycopg.connect(host=app.config['DB_SERVER'],
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            cur.execute('INSERT INTO coach (username, passwd,fio,gender,bodyweight,height,age,social_media,achievements)' # добавление нового пользователя в базу данных
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (login,password_hash,fio,gender,weight,height,age,media,achv))
        # создать запись в таблице используя password_hash
        flash(f'Регистрация {reg_form.username.data} успешна', 'success')
        return redirect(url_for('CO_login'))
    return render_template('CO_registration.html', title='Регистрация тренера', form=reg_form) # вывод страницы регистрации


from werkzeug.security import check_password_hash
from app.forms import LoginForm
from app.user import User
from flask import render_template, redirect, flash, url_for
from flask_login import login_user, current_user
from urllib.parse import urlsplit

@app.route('/login', methods=['GET', 'POST']) # авторизация спортсмена
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            res = cur.execute('SELECT username, passwd '
                              'FROM "athlete" '
                              'WHERE username = %s', (login_form.username.data,)).fetchone() # выбор пользователя с соответстсвующими данными
        if res is None or not check_password_hash(res[1], login_form.password.data): # проверка пароля
            flash('Попытка входа неудачна', 'danger')
            return redirect(url_for('login'))
        role = 1
        id = res[0]
        username, password = res
        user = User(id, username, password, role)
        login_user(user, remember=login_form.remember_me.data)
        next = request.args.get('next')
        if not next or urlsplit (next).netloc != '':
            next = url_for('index')
        flash(f'Вы успешно вошли в систему, {current_user.username}', 'danger')
        return redirect(next)
    return render_template('login.html', title='Авторизация спортсмена', form=login_form) # вывод страницы авторизации

@app.route('/CO_login', methods=['GET', 'POST']) # авторизация тренера
def CO_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            res = cur.execute('SELECT username, passwd '
                              'FROM "coach" '
                              'WHERE username = %s', (login_form.username.data,)).fetchone() # выбор пользователя с соответстсвующими данными
        if res is None or not check_password_hash(res[1], login_form.password.data): # проверка пароля
            flash('Попытка входа неудачна', 'danger')
            return redirect(url_for('CO_login'))
        role = 2
        id ='_CO_'+res[0] # указатель, что это id тренера
        username, password = res
        user = User(id, username, password, role)
        login_user(user, remember=login_form.remember_me.data)
        next = request.args.get('next')
        if not next or urlsplit (next).netloc != '':
            next = url_for('index')
        flash(f'Вы успешно вошли в систему, {current_user.username}', 'danger')
        return redirect(next)
    return render_template('login.html', title='Авторизация тренера', form=login_form) # вывод страницы авторизации

from app import app
from flask_login import logout_user
from flask import redirect, url_for

@app.route('/logout') # выход из учетной записи
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route ('/records')
def show_records():
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        records = cur.execute(f'SELECT nazv, world_record_men, world_record_women FROM exercise').fetchall() # выбор мировых рекордов из таблицы с упражнениями 
    return render_template('records.html',recs=records) # вывод страницы с рекордами


from flask import render_template, abort
from flask_login import current_user, login_required
@app.route('/profile/<username>') # профиль спортсмена
@login_required
def profile(username):
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        res = cur.execute('SELECT fio, gender, bodyweight, height, age, social_media '
                    'FROM "athlete" '
                    'WHERE username = %s', (username,)).fetchone()  # вывод данных спортсмена
        exc = cur.execute('SELECT username, exercise_name, weight_kg, reps_count, one_rpm, execution_date '
                    'FROM "athlete_result" '
                    'WHERE username = %s ORDER BY exercise_name ASC, execution_date DESC', (username,)).fetchall() # вывод результатов спортсмена
    fio,gender,weight,height,age,socialmedia = res
    results = exc

    return render_template('profile.html',fio = fio,gender = gender,weight = weight,height = height,
                           age = age ,socialmedia = socialmedia, results = results, profile_username = username) # вывод страницы профиля


def format_datetime_for_url(post_datetime):
    # Преобразуем строку даты и времени в формат, безопасный для URL
    # Например, заменим все знаки на нижние подчеркивания
    b = str(post_datetime)
    b = b.replace(" ","_")
    b = b.replace(":","_")
    return b
def datetime_from_url(b):
    l1 = list(b)
    l1[10] = ' '
    l1[13] = ':'
    l1[16] = ':'
    b = ''.join(l1)
    return b

@app.route('/CO_profile/<username>') # профиль тренера
@login_required
def CO_profile(username):
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        res = cur.execute('SELECT fio, gender, bodyweight, height, age, social_media, achievements '
                    'FROM "coach" '
                    'WHERE username = %s', (username,)).fetchone() # вывод данных тренера
        exc = cur.execute('SELECT username, exercise_name, weight_kg, reps_count, one_rpm, execution_date '
                    'FROM "coach_result" '
                    'WHERE username = %s', (username,)).fetchall() # вывод результатов тренера
        prg = cur.execute('SELECT nazv, publication_datetime, text ' 
                          'FROM "publication" '
                          'WHERE author_username = %s', (username,)).fetchall() # вывод публикаций
        ath_ratings = cur.execute ('SELECT * '
                    'FROM "athlete_rating" '
                    'WHERE author_username = %s', (username,)).fetchall() # вывод отзывов спортсменов
        coach_ratings = cur.execute ('SELECT * '
                    'FROM "coach_rating" '
                    'WHERE author_username = %s', (username,)).fetchall() # вывод отзывов тренеров
    fio,gender,weight,height,age,socialmedia,achv = res
    results = exc
    posts = prg

    return render_template('CO_profile.html',fio = fio,gender = gender,weight = weight,height = height,
                           age = age ,socialmedia = socialmedia, achv = achv, results = results, posts = posts, 
                           profile_username = username, format_datetime_for_url = format_datetime_for_url, ath_ratings = ath_ratings, coach_ratings = coach_ratings) # страница профиля тренера

from app.forms import EditProfileForm,CO_EditProfileForm
from flask import redirect, flash, url_for

@app.route('/edit', methods=['GET', 'POST']) # редактирование профиля
@login_required
def edit_user():
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        if current_user.role == 1: # если это спортсмен, то достаём данные профиля из таблицы с спортсменами
            res = cur.execute('SELECT fio, gender, bodyweight, height, age, social_media '
                        'FROM "athlete" '
                        'WHERE username = %s', (current_user.username,)).fetchone()
            fio,gender,weight,height,age,socialmedia = res
            form = EditProfileForm(FIO=fio, weight = weight, height = height, age = age, media = socialmedia, gender = gender) 
        elif current_user.role == 2: # если это тренер, то достаём данные профиля из таблицы с тренерами
            res = cur.execute('SELECT fio, gender, bodyweight, height, age, social_media, achievements '
                        'FROM "coach" '
                        'WHERE username = %s', (current_user.username,)).fetchone()
            fio, gender, weight,height,age,socialmedia,achievements = res
            form = CO_EditProfileForm(FIO=fio, weight = weight, height = height, age = age, media = socialmedia, gender = gender,achv = achievements)
        
    if form.validate_on_submit():
        fio = form.FIO.data # получение данных из формы
        gender = form.gender.data
        weight = form.weight.data
        height = form.height.data
        age = form.age.data
        socialmedia = form.media.data
        if current_user.role == 2: # если тренер, то можно ещё изменить данные об индивидуальных достижениях
            achievements = form.achv.data
        print(fio)
        with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                         user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            if current_user.role == 1:# если спортсмен, то редактируем таблицу спорстмена
                cur.execute('UPDATE athlete SET fio =%s, gender = %s, bodyweight =%s, height = %s, age = %s, social_media = %s WHERE username =%s',
                            (fio,gender,weight,height,age,socialmedia,current_user.username)) 
            elif current_user.role == 2:# если тренер, то редактируем таблицу тренера
                cur.execute('UPDATE coach SET fio =%s, gender= %s, bodyweight =%s, height = %s, age = %s, social_media = %s, achievements = %s WHERE username =%s',
                            (fio,gender,weight,height,age,socialmedia,achievements,current_user.username))
        print(fio)    
        # сохранить новые данные пользователя в базе данных
        flash('Изменения сохранены')
        if current_user.role == 1:# если спортсмен, то переход в профиль спортсмена
            return redirect(url_for('profile', username = current_user.username ))
        elif current_user.role == 2: # если тренер, то переход в профиль тренера
            return redirect(url_for('CO_profile', username = current_user.username))
    else:
        print('fail')
    return render_template('edit.html', title='Редактирование пользователя', form=form)

from app.forms import AddResult
import datetime
@app.route('/add_result', methods=['GET', 'POST']) # добавить результат упражения
@login_required
def add_result():
    add_form = AddResult()
    if add_form.validate_on_submit():
        now = datetime.datetime.now()
        username = current_user.username # получение данных из формы
        execution_date = now.strftime("%Y-%m-%d %H:%M:%S") # преобразование даты в нужный формат
        excercise_name = add_form.excercise.data
        weight = add_form.weight.data
        reps = add_form.reps.data
        print(execution_date)
        if weight == None: # рассчёт одноповторного максимума
            ONE_REP_MAX = 0
        elif (reps == 1):
            ONE_REP_MAX = weight
        else:
            ONE_REP_MAX = weight*(1+0.0333*reps)
        with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                            user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            if current_user.role == 1: # если спортсмен, то добавляем в таблицу для спортсмена
                cur.execute('INSERT INTO athlete_result '
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            (username,excercise_name,execution_date,weight,reps, ONE_REP_MAX))
                return redirect(url_for('profile',username = username))
            elif current_user.role == 2:# если тренер, то добавляем в таблицу для тренера
                cur.execute('INSERT INTO coach_result '
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            (username,excercise_name,execution_date,weight,reps, ONE_REP_MAX))
                return redirect(url_for('CO_profile',username = username))
    return render_template('add_result.html',form = add_form)

from app.forms import AddPost
@app.route('/upload', methods=['GET', 'POST']) # загрузить публикацию
@login_required
def add_post():
    add_form = AddPost()
    if current_user.role != 2: # проверка роли, если не тренер, то добавить публикацию нельзя
        abort(403)
    if add_form.validate_on_submit():
        username = current_user.username # получение данных из формы
        nazv = add_form.nazv.data 
        text = add_form.Text.data
        now = datetime.datetime.now()
        publication_date = now.strftime("%Y-%m-%d %H:%M:%S") # преобразование даты в нужный формат
        with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                            user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            cur.execute('INSERT INTO publication '
                        'VALUES (%s, %s,%s,%s)',
                        (username,publication_date,text,nazv)) # добавление публикации в бд
        return redirect(url_for('CO_profile',username = username))
    return render_template('upload.html',form = add_form)    

@app.route('/standards', methods=['GET', 'POST']) # силовые стандарты
def get_standards():
    with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                            user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            stnd = cur.execute('SELECT * '
                    'FROM "standards" ORDER BY exercise_name ASC, gender DESC, bodyweight_ratio DESC').fetchall() #
    return render_template('standards.html',standards = stnd)

from app.forms import RateForm
@app.route('/CO_profile/<username>/add_rating/<dat>', methods=['GET', 'POST']) # добавление отзыва на публикацию в профиле тренера
@login_required
def add_rating(username,dat):
    print(f"username: {username}, dat: {dat}")
    form = RateForm()
    b = datetime_from_url(dat)

    if form.validate_on_submit():
        b = datetime_from_url(dat)
        print ('yes')
        rating = form.rating.data
        comment = form.comment.data
        with psycopg.connect(host=app.config['DB_SERVER'], # подключение к бд
                                user=app.config['DB_USER'],
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                rev = current_user.username
                author = username
                publication_date = cur.execute('SELECT publication_datetime ' 
                            'FROM "publication" '
                            'WHERE author_username = %s AND publication_datetime = %s ' , (username, b)).fetchall() #
                if current_user.role == 1: # если спортсмен, то добавляем отзыв в отзывы спортсменов
                    cur.execute('INSERT INTO athlete_rating ' 
                                'VALUES (%s,%s,%s,%s,%s)',
                                (rev,author,publication_date,rating,comment))
                elif current_user.role == 2: # если тренер, то добавляем отзыв в отзывы тренеров
                    cur.execute('INSERT INTO coach_rating ' 
                                'VALUES (%s,%s,%s,%s,%s)',
                                (rev,author,publication_date,rating,comment))
        return redirect(url_for('CO_profile',username = username))
    return render_template('add_review.html',public_date = b , form = form)
