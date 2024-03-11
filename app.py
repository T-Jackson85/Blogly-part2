"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Users, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:aniya123///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
db.create_all()

@app.route("/")
def home():
    """Homepage shows list of all users"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return redirect("homepage.html", posts= posts)

@app.route('/users')
def user_list():
    """Shows user info"""

    users= Users.query.order_by(Users.last_name, Users.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():

    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def new_users():

    new_user= Users(
        first_name= request.form['first_name'],
        last_name= request.form['last_name'],
        image_url= request.form['image-url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:users_id>')
def show_user(users_id):

    users = Users.query.get_or_404(users_id)
    return render_template('users/show.html', users=users)

@app.route('/users/<int:users_id>/edit', methods=["POST"])
def users_update(users_id):

    user = Users.query.get_or_404(users_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:users_id>/posts/new')
def new_post_form(users_id):

    users = Users.query.get_or_404(users_id)
    return render_template('new.html', users= users)

@app.route('/users/<int:users_id>/posts/new', methods=['POST'])
def new_post(users_id):

    users = Users.query.get_or_404(users_id)
    new_post = Post(title = request.form['content'],users =users)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{users_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template('show.html', post= post)

@app.route('/post/<int:post_id>/edit')
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('edit.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['POST'])
def edited_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")





if __name__== "__main__":
     app.run(debug=True)
