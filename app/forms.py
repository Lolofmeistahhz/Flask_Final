from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

from app.models import Menu


class OrderForm(FlaskForm):
    order_name = StringField('order_name', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    adress = StringField('adress', validators=[DataRequired()])
    dish1 = SelectField(default=1)
    dish2 = SelectField(default=1)
    dish3 = SelectField(default=1)
    dish4 = SelectField(default=1)
    dish5 = SelectField(default=1)
    amount = IntegerField()
    submit1 = SubmitField('Сделать заказ', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.dish1.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish2.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish3.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish4.choices = [(c.id, c.name) for c in Menu.query.all()]
        self.dish5.choices = [(c.id, c.name) for c in Menu.query.all()]


class OrderSatus(FlaskForm):
    search = StringField('search')
    submit = SubmitField('Поиск', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(OrderSatus, self).__init__(*args, **kwargs)
