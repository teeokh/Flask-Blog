from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

app = Flask(__name__) # name = special variable that is the name of the module. Instantiates the module
app.config.from_object(Config)
db = SQLAlchemy(app) # Actually initialising an instance of the SQLAlchemy class
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from flaskblog.users.routes import users # Needs to be at bottom to prevent another circular import 
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)