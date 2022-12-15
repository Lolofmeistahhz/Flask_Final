from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app import db, app


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    pasword = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"
    def set_password(self, password):
        self.pasword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pasword, password)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<posts {self.id}>"


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(500),nullable=True)

    def __repr__(self):
        return f"<menu {self.id}>"


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    adress = db.Column(db.String(255), nullable=False)
    order_data = db.Column(db.DateTime, default=datetime.utcnow)
    dish1 = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    dish2 = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    dish3 = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    dish4 = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    dish5 = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30),nullable = False)
    def __repr__(self):
        return f"<orders {self.id}>"


with app.app_context():
    db.create_all()
