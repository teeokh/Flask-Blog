from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # If there is no duplicate, then nothing will be returned
        if user:
            raise ValidationError(f'{username.data} is taken. Please choose a different one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() # If there is no duplicate, then nothing will be returned
        if user:
            raise ValidationError(f'{email.data} is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username: # This allows user to submit empty form. It only checks for duplicate if the submitted data is different to their current data (rather than checking for their username in db and finding it autmoatically)
            user = User.query.filter_by(username=username.data).first() # If there is no duplicate, then nothing will be returned
            if user:
                raise ValidationError(f'{username.data} is taken. Please choose a different one')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() # If there is no duplicate, then nothing will be returned
            if user:
                raise ValidationError(f'{email.data} is taken. Please choose a different one') 
            
class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit = SubmitField('Post')