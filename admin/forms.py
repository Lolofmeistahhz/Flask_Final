from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Вход')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, *kwargs)


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])
    submit = SubmitField('Сохранить', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)


class DishForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = IntegerField('price', default=0)
    photo = FileField('photo')
    submit = SubmitField('Сохранить', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
