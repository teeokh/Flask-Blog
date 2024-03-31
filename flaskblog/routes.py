import secrets, os
from flaskblog.models import User, Post
from PIL import Image
from flask import abort, render_template, request, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/") # This allows us to tell Flask what URL to trigger. Returns the information shown on the page
@app.route("/home") # Adding another decorator for same function
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about") # This allows us to tell Flask what URL to trigger. Returns the information shown on the page
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You are now able to log in', 'success') # In flask-WTF, the input data in StringFields is labelled as 'data'. Flash function will show something on the screen once
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # If user exists and password is valid (checking db password vs form password)
            login_user(user, remember=form.remember.data)
            flash("Login successful!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful! Please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) # Takes the picture entered by the user and gets the file, then updates their picture
            current_user.image_file = picture_file
        current_user.username = form.username.data # Updates the database with the form entry
        current_user.email = form.email.data # Updates the database with the form entry
        db.session.commit()
        flash(f'Your account has been updated', 'success')
        return redirect (url_for('account')) # Important to have redirect (POST GET REDIRECT PATTERN = confirm resubmission, don't want this)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # Grabs specific post form database
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user: # Only the current user can update their post
        abort(403) # 403 = forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # Don't need to add, as post is already in database
        flash("your post has been updated!", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user: # Only the current user can update their post
        abort(403) # 403 = forbidden route
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('home'))