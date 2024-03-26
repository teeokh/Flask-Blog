from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app

posts = [ # List of dictionaries for post content
    {
        'author': 'Terrell Okhiria',
        'title': 'Blog Post 1',
        'content': 'First blog post content',
        'date_posted': '15th March 2024'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second blog post content',
        'date_posted': '8th March 2024'
    }
]

@app.route("/") # This allows us to tell Flask what URL to trigger. Returns the information shown on the page
@app.route("/home") # Adding another decorator for same function
def home():
    return render_template('home.html', posts=posts)

@app.route("/about") # This allows us to tell Flask what URL to trigger. Returns the information shown on the page
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success') # In flask-WTF, the input data in StringFields is labelled as 'data'. Flash function will show something on the screen once
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful! Please check username and password", 'danger')
    return render_template('login.html', title='Login', form=form)