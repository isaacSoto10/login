from enum import unique
from operator import length_hint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db= SQLAlchemy()

bcrypt= Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    __tablename__ = 'usuarios'

    username= db.Column(db.String, primary_key=True, length=20, unique=True)
    password= db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False, unique=True, length=50)
    first_name= db.Column(db.String, nullable=False, length=30)
    last_name= db.Column(db.String, nullable=False, length=30)


    @classmethod
    def register(cls, username, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        username = User.query.filter_by(username=username).first()
        if username and bcrypt.check_password_hash(username.password, password):
            return username
        else: 
            return False


class feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, length=100)
    content = db.column(db.Text, nullable=False)
    username = db.column()



