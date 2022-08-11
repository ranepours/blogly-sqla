from flask import Flask, request, render_template, redirect
from models import connect_db, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key'

connect_db(app)

@app.route('/')
def list_users():
    """RENDER ALL USERS IN DB/APP"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)

@app.route('/create-user')
def show_form():
    """RENDER FORM TO ADD NEW USER TO DB"""
    return render_template('create.html')

@app.route('/create-user', methods=["POST"])
# add new user into db
def add_new():
    """CREATE NEW USER"""
    new_user=User(first_name=request.form['first_name'], last_name=request.form['last_name'], img_url=request.form['img_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:users_id>')
def render_user(users_id):
    """RENDER USER INFO PAGE"""
    user=User.query.get_or_404(users_id)
    return render_template('render.html', user=user)

@app.route('/users/edit/<int:users_id>')
def mod(users_id):
    """RENDER EDITS PAGE"""
    user = User.query.get_or_404(users_id)
    return render_template('mod.html', user=user)

@app.route('/users/edit/<int:users_id>', methods=["POST"])
def update(users_id):
    """HANDLE EDITS"""
    user = User.query.get_or_404(users_id)
    user.first_name=request.form['first_name']
    user.last_name=request.form['last_name']
    user.img_url=request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/delete/<int:users_id>', methods=["POST"])
def delete(users_id):
    """REMOVE USER FROM DB"""
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')