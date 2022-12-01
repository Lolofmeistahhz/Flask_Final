from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)
app.config.from_object('config')


db: SQLAlchemy = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)



from app import views