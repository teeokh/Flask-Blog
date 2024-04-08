from flask import Blueprint
from flaskblog.models import User, Post
from flask import render_template, request, url_for, flash, redirect
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__) # Initialise an instance of Blueprint, pass in name of the blueprint 

@users.route("/register", methods=['GET', 'POST'])
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

@users.route("/login", methods=['GET', 'POST'])
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

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route("/account", methods=['GET', 'POST'])
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


@users.route("/user/<string:username>") # Means the string part after the 'user' in the url will be captured as the username
def user_posts(username):
    page = request.args.get('page', 1, type=int) # This requests the 'page' part of the url, and defaults it to 1
    user = User.query.filter_by(username=username).first_or_404() # If username isn't found in database, returns 404. Otherwise, makes that user 'user'
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3) # Retrieve the posts created by that username using 'author'. Order the posts by descending date, and 3 posts per page
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Grabs first user that has the email entered in the Request form
        send_reset_email(user)
        flash("An email has been sent with instructions on how to reset your password.", 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token) # Gets the token from this method in the User class
    if user is None: # If no user_id is returned i.e. token is expired or wrong
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in.', 'success') # In flask-WTF, the input data in StringFields is labelled as 'data'. Flash function will show something on the screen once
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form) # Renders template to reset password (if token is valid)
