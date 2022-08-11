from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for User"""
    def setUp(self):
        User.query.delete()
        user = User(first_name="Dummy", last_name="User", img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMG2pyKV_KchHPCOehKXLebjYiOLgRhMObxw&usqp=CAU")

        db.session.add(user)
        db.session.commit()

        self.user_id=user.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Dummy User", html)

    def test_show_user(self):
        with app.test_client() as client:
            res  = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Dummy User</h1>', html)
            self.assertIn(self.user.first_name, html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'first_name': "Tonto", 'last_name': 'Personaje'}
            res = client.post('/', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Tonto Personaje</h1>', html)
