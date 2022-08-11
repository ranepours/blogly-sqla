from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Post, Tag

########################################
##############PART ONE##################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key'

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def render_home():
    """render homepage (PART TWO)"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route('/users')
def list_users():
    """RENDER ALL USERS IN DB/APP"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)

@app.route('/users/new', methods=["GET"])
def show_form():
    """RENDER FORM TO ADD NEW USER TO DB"""
    return render_template('create.html')

@app.route('/users/new', methods=["POST"])
# add new user into db
def add_new():
    """CREATE NEW USER"""
    new_user=User(
        first_name=request.form['first_name'], 
        last_name=request.form['last_name'], 
        img_url=request.form['img_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>')
def render_user(users_id):
    """RENDER USER INFO PAGE"""
    user=User.query.get_or_404(users_id)
    return render_template('render.html', user=user)

@app.route('/users/<int:users_id>/edit', methods=["GET"])
def mod(users_id):
    """RENDER EDITS PAGE"""
    user=User.query.get_or_404(users_id)
    return render_template('mod.html', user=user)

@app.route('/users/<int:users_id>/edit', methods=["POST"])
def update(users_id):
    """HANDLE EDITS"""
    user=User.query.get_or_404(users_id)
    user.first_name=request.form['first_name']
    user.last_name=request.form['last_name']
    user.img_url=request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete_user(users_id):
    """REMOVE USER FROM DB"""
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


########################################
##############PART TWO##################
@app.route('/users/<int:users_id>/posts/new')
def new_post_form(users_id):
    """render form to create new post from user"""
    user=User.query.get_or_404(users_id)
    tags=Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:users_id>/posts/new', methods=["POST"])
def handle_post(users_id):
    """handle new post form"""
    user = User.query.get_or_404(users_id)
    tag_ids=[int(num) for num in request.form.getlist("tags")]
    tags=Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post=Post(
                title=request.form['title'], 
                content=request.form['content'], 
                user=user, 
                tags=tags)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{users_id}')

@app.route('/posts/<int:post_id>')
def render_post(post_id):
    """render post & post info"""
    post=Post.query.get_or_404(post_id)
    return render_template('post_page.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def edit_post(post_id):
    """render edit post form"""
    post=Post.query.get_or_404(post_id)
    tags=Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """handle edit; redirect to post views"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids=[int(num) for num in request.form.getlist("tags")]
    post.tags=Tag.query.filter(Tag.id.in_(tag_ids)).all()

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
@app.route("/tags")
def tags():
    """render ALL tags"""
    tags=Tag.query.all()
    return render_template('all_tags.html',tags=tags)

@app.route("/tags/<int:tag_id>")
def render_tag(tag_id):
    """render tag page"""
    tag=Tag.query.get_or_404(tag_id)
    return render_template('render_tag.html',tag=tag)

@app.route('/tags/new', methods=["GET"])
def new_tag():
    """render new tag form"""
    posts=Post.query.all()
    return render_template('new_tag.html',posts=posts)

@app.route('/tags/new', methods=["POST"])
def handle_new_tag():
    """handle new tag"""
    post_ids=[int(num) for num in request.form.getlist("posts")]
    posts=Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag=Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def edit_tag(tag_id):
    """render edit tag form"""
    tag=Tag.query.get_or_404(tag_id)
    posts=Post.query.all()
    return render_template('tag_edit.html',tag=tag,posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """handle tag edits"""
    tag=Tag.query.get_or_404(tag_id)
    tag.name=request.form['name']
    post_ids=[int(num) for num in request.form.getlist("posts")]
    tag.posts=Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """handle tag delete"""
    tag=Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')