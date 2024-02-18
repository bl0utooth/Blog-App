"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post 

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_app_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bluprint'


toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def root():
    return redirect("/users")



@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



@app.route('/users/<int:user_id>/posts/new')
def post_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_posts(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
    content=request.form['content'],
    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Posted! '{new_post.title}'")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:user_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Changes to the Post:'{post.title}' have been made.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post: '{post.title}' has been deleted.")

    return redirect(f"/users/{post.user_id}")