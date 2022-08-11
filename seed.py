from models import User, Post, db
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

pa = Post(author=1,title="Deaf?",content="You're deaf? You don't look deaf.")
pb = Post(author=5,title="Deaf",content="You don't look ignorant but I guess you can't judge a book by it's cover right?")
pc = Post(author=5,title="",content="")
pd = Post(author=4,title="Buy your friends",content="At least we don't buy our friends with our daddy's bank account")
pe = Post(author=3,title="Cheer",content="I'm not a snob, I'm just better than you are, yeah!")
pf = Post(author=2,title="No dad",content="All because you don't have a dad OR a bank account!")

db.session.add_all([pa, pb, pc, pd, pe, pf])
db.session.commit()