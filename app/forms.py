from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length

from app.models import Menu


class OrderForm(FlaskForm):
    order_name = StringField('order_name', validators=[DataRequired(),Length(min=4,max=100)])
    phone = StringField('phone',validators=[DataRequired(),Length(max=11)])
    adress = StringField('adress',validators=[DataRequired(),Length(min=10,max=255)])
    dish1 = SelectField()
    dish2 = SelectField()
    dish3 = SelectField()
    dish4 = SelectField()
    dish5 = SelectField()
    amount = IntegerField()
    status = SelectField()
    submit1 = SubmitField('Рассчитать стоимость заказа',validators=[DataRequired()])
    submit2 = SubmitField('Сделать заказ')


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.dish1.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish2.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish3.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish4.choices = [(c.id,c.name)for c in Menu.query.all()]
        self.dish5.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.status.choices = [('В обработке','В обработке'),('На кухне','На кухне'),('На доставке','На доставке')]


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(),Length(min=4,max=50)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=4)])
    submit = SubmitField('Вход')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, *kwargs)

class RegisterForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(),Length(min=4,max=50)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=4)])
    submit = SubmitField('Вход')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, *kwargs)