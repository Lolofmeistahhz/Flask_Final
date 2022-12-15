from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, SelectField
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


class OrderSatus(FlaskForm):
    status = SelectField()
    submit = SubmitField('Изменить статус', validators=[DataRequired()])


    def __init__(self, *args, **kwargs):
        super(OrderSatus, self).__init__(*args, **kwargs)
        self.status.choices = [('В обработке','В обработке'),('Принят в работу','Принят в работу'),('На доставке','На доставке'),('Выполнен','Выполнен'),('Отклонен','Отклонен')]

class DishForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = IntegerField('price', default=0)
    photo = FileField('photo')
    submit = SubmitField('Сохранить', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
