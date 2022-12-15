from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, validators
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(),Length(min=4,max=50)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=4)])
    submit = SubmitField('Вход')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, *kwargs)


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(),Length(min=3,max=100)])
    text = StringField('text', validators=[DataRequired(),Length(min=10,max=500)])
    submit = SubmitField('Сохранить', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)


class DishForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(),Length(min=4,max=100)])
    description = StringField('description', validators=[DataRequired(),Length(min=10,max=500)])
    price = IntegerField('price', default=0)
    photo = FileField('photo')
    submit = SubmitField('Сохранить', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
