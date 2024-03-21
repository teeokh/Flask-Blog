from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__) # name = special variable that is the name of the module. Instantiates the module

app.config['SECRET_KEY'] = 'cb411410f7328c85eb01ca752b487c36'

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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__== '__main__':
    app.run(debug=True)