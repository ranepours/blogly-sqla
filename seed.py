from models import User, db
from app import app

db.drop_all()
db.create_all()

user1 = User(first_name="Yasmin", last_name="Bratz")
user2 = User(first_name="Sasha", last_name="Bratz")
user3 = User(first_name="Jade", last_name="Bratz")
user4 = User(first_name="Cloe", last_name="Bratz")
user5 = User(first_name="Dylan", last_name="Bratz")
user6 = User(first_name="Kobe", last_name="Bratz")

db.session.add_all([user1,user2,user3,user4,user5,user6])
db.session.commit()