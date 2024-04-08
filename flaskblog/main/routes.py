from flask import Blueprint
from flaskblog.models import Post
from flask import render_template, request

main = Blueprint('main', __name__)

@main.route("/") # This allows us to tell Flask what URL to trigger. Returns the information shown on the page
@main.route("/home") # Adding another decorator for same function
def home():
    page = request.args.get('page', 1, type=int) # This requests the 'page' part of the url, and defaults it to 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3) # Order the posts by descending date, and 3 posts per page
    return render_template('home.html', posts=posts)

@main.route("/about") # This allows us to tell Flask what URL to trigger. Returns the information shown on the page
def about():
    return render_template('about.html', title='About')