from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO']= 'FALSE'

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """test model for users"""
    def setUp(self):
        """clean up existing data"""
        User.query.delete()
    def tearDown(self):
        """clean up fouled"""
        db.session.rollback()
    def test_exist(self):
        """user is properly added to db"""
        user = User(first_name="Dummy", last_name="User", img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMG2pyKV_KchHPCOehKXLebjYiOLgRhMObxw&usqp=CAU")
        self.assertEquals(user.first_name, "Dummy")
