from flask_sqlalchemy import SQLAlchemy

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

    @property
    def full_name(self):
        """Full name render"""
        return f"{self.first_name} {self.last_name}"