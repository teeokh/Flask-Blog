from flaskblog import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, timezone
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # Grabs user id from db, and returns it as an integer

class User(db.Model, UserMixin): # We create the User class
    id = db.Column(db.Integer, primary_key=True) # primary_key=True means this will be unique to our user
    username = db.Column(db.String(20), unique=True, nullable=False) # nullable = cannot be null, there must be an input. Max characters = 20
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # Max image hash = 20 characters. Default will be if user doesn't choose a profile pic
    password = db.Column(db.String(60), nullable=False) 
    posts = db.relationship('Post', backref='author', lazy=True) 

    def get_reset_token(self, expires_sec=1800): # self means can have access to the User class attributes + methods
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) # Serializer generates the token using the user's secret key
        return s.dumps({'user_id' : self.id}).decode('utf-8') # Returns the token using the dictionary of user_id with id value, and decodes into a string

    @staticmethod # Means no need for 'self' in this method (as user already handled in previous method)
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY']) # Creates instance of Serializer with same secret key
        try:
            user_id = s.loads(token)['user_id'] # Deserializes the token so that it can return the user_id held in the dictionary that belongs to the token
        except:
            return None # If token is invalid or expired
        return User.query.get(user_id)


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