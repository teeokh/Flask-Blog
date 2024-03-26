from flaskblog import db
from datetime import datetime, timezone

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