from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, DateField, IntegerField, FloatField, PasswordField, SubmitField, SelectField, validators
#форма регистрации спортсмена
class ATH_RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25)])
    password = PasswordField('Пароль', [validators.InputRequired(),
                                        validators.Length(min=6, max=100),
                                        validators.EqualTo('confirm', message='Пароли должны совпадать')])
    confirm  = PasswordField('Повторите пароль')
    age = IntegerField('Возраст', [validators.InputRequired()])
    FIO = StringField('ФИО', [validators.Length(min=4, max=100),validators.Optional()])
    height = FloatField('Рост в см', [validators.InputRequired()])
    weight = FloatField('Масса в кг', [validators.InputRequired()])
    media = StringField('Ссылка на соцсети', [validators.Length(min=4, max=100),validators.Optional()])
    gender = SelectField('Пол (муж или жен)', choices=[('муж'),('жен')])
    submit = SubmitField('Зарегистрироваться')
#форма регистрации тренера
class CO_RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25)])
    password = PasswordField('Пароль', [validators.InputRequired(),
                                        validators.Length(min=6, max=100),
                                        validators.EqualTo('confirm', message='Пароли должны совпадать')])
    confirm  = PasswordField('Повторите пароль')
    age = IntegerField('Возраст', [validators.InputRequired()])
    FIO = StringField('ФИО', [validators.Length(min=4, max=100),validators.Optional()])
    height = FloatField('Рост в см', [validators.InputRequired()])
    weight = FloatField('Масса в кг', [validators.InputRequired()])
    media = StringField('Ссылка на соцсети', [validators.Length(min=4, max=100),validators.Optional()])
    achv = StringField('Индивидуальные достижения', [validators.Length(min=4, max=500),validators.Optional()])
    gender = SelectField('Пол (муж или жен)', choices=[('муж'),('жен')])
    submit = SubmitField('Зарегистрироваться')
#форма редактирования профиля спортсмена
class EditProfileForm(FlaskForm):
    age = IntegerField('Возраст')
    FIO = StringField('ФИО')
    gender = SelectField('Пол (муж или жен)', choices=[('муж'),('жен')])
    height = FloatField('Рост в см')
    weight = FloatField('Масса в кг')
    media = StringField('Ссылка на соцсети')
    submit = SubmitField('Сохранить')
#форма редактирования профиля тренера
class CO_EditProfileForm(FlaskForm):
    age = IntegerField('Возраст')
    FIO = StringField('ФИО')
    gender = SelectField('Пол (муж или жен)', choices=[('муж'),('жен')])
    height = FloatField('Рост в см')
    weight = FloatField('Масса в кг')
    media = StringField('Ссылка на соцсети')
    achv = StringField('Индивидуальные достижения')
    submit = SubmitField('Сохранить')
#форма авторизации
class LoginForm(FlaskForm):
    username = StringField('Логин', [validators.InputRequired()])
    password = PasswordField('Пароль', [validators.InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
#форма добавления результата
class AddResult(FlaskForm):
    excercise = SelectField('Упражнение', choices=[('жим лёжа'),('приседания со штангой'),
                                                   ('становая тяга'),('подъём гантелей на бицепс'),
                                                   ('жим гантелей над головой'),('подтягивания'),
                                                   ('подтягивания с дополнительным отягощением'),('тяга вертикального блока'),
                                                   ('тяга горизонтального блока'),('ягодичный мостик')],validate_choice=True)
    weight = FloatField('Вес в кг', [validators.Optional()])
    reps = IntegerField('Количество повторений')
    submit = SubmitField('Добавить')
#форма добавления публикации
class AddPost(FlaskForm):
    nazv = StringField('Введите название публикации')
    Text = StringField('Введите текст вашей публикации')
    submit = SubmitField('Запостить!')
#форма добавления отзыва
class RateForm (FlaskForm):
    rating = SelectField('Выберите оценку (от 1 до 5 звёзд)', choices=[(1),(2),(3),(4),(5)],validate_choice=True)
    comment = StringField('Ваши комментарии',[validators.Optional()])
    submit = SubmitField('Оценить')