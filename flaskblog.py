from datetime import datetime, timezone
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import os

app = Flask(__name__) # name = special variable that is the name of the module. Instantiates the module
app.config['SECRET_KEY'] = 'cb411410f7328c85eb01ca752b487c36'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Configuring the flask app to use SQLite as the SLQ for the database and specifies the database file (site.db) /// gives the path relative to the directory we're currently in
db = SQLAlchemy(app) # Actually initialising an instance of the SQLAlchemy class

class User(db.Model): # We create the User class
    id = db.Column(db.Integer, primary_key=True) # primary_key=True means this will be unique to our user
    username = db.Column(db.String(20), unique=True, nullable=False) # nullable = cannot be null, there must be an input. Max characters = 20
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # Max image hash = 20 characters. Default will be if user doesn't choose a profile pic
    password = db.Column(db.String(60), nullable=False) 
    posts = db.relationship('Post', backref='author', lazy=True) 

    def __repr__(self): # Allows us to control what is printed when an object of the class is printed
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model): # We create the Post class
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # This is the ID of the user that authored the post

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

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

if __name__== '__main__':
    app.run(debug=True)