import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

# connect db to flask app
def connect_db(app):
    db.app = app
    db.init_app(app)

IMG_DEFAULT = "https://preview.redd.it/h5gnz1ji36o61.png?width=225&format=png&auto=webp&s=84379f8d3bbe593a2e863c438cd03e84c8a474fa"

# models::::
class User(db.Model):
    """users table model for app"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, default=IMG_DEFAULT)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Full name render"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """posts associated w/ users in db"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    @property
    def date(self):
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")