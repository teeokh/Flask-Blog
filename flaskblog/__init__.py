from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # name = special variable that is the name of the module. Instantiates the module
app.config['SECRET_KEY'] = 'cb411410f7328c85eb01ca752b487c36'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Configuring the flask app to use SQLite as the SLQ for the database and specifies the database file (site.db) /// gives the path relative to the directory we're currently in
db = SQLAlchemy(app) # Actually initialising an instance of the SQLAlchemy class
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes # Needs to be at bottom to prevent another circular import 