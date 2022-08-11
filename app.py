from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Post

########################################
##############PART ONE##################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key'

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/users')
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

    return redirect('/users')

@app.route('/users/<int:users_id>')
def render_user(users_id):
    """RENDER USER INFO PAGE"""
    user=User.query.get_or_404(users_id)
    return render_template('render.html', user=user)

@app.route('/users/<int:users_id>/edit')
def mod(users_id):
    """RENDER EDITS PAGE"""
    user = User.query.get_or_404(users_id)
    return render_template('mod.html', user=user)

@app.route('/users/<int:users_id>/edit', methods=["POST"])
def update(users_id):
    """HANDLE EDITS"""
    user = User.query.get_or_404(users_id)
    user.first_name=request.form['first_name']
    user.last_name=request.form['last_name']
    user.img_url=request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete(users_id):
    """REMOVE USER FROM DB"""
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


########################################
##############PART TWO##################
@app.route('/users/<int:users_id>/posts/new')
def new_post_form(user_id):
    """render form to create new post from user"""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('users/<int:users_id>/posts/new', methods=["POST"])
def handle_post(user_id):
    """handle new post form"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('posts/<int:post_id>')
def render_post(post_id):
    """render post"""
    post=Post.query.get_or_404(post_id)
    return render_template('post_page.html', post=post)

@app.route('posts/<int:post_id>/edit', methods=["GET"])
def edit_post(post_id):
    """render edit post form"""
    post=Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """handle edit; redirect to post views"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """delete post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

########################################
############PART THREE##################