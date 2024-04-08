from flask import Blueprint
from flaskblog.models import Post
from flask import abort, render_template, request, url_for, flash, redirect
from flaskblog.posts.forms import PostForm
from flaskblog import db
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                           form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # Grabs specific post form database
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user: # Only the current user can update their post
        abort(403) # 403 = forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # Don't need to add, as post is already in database
        flash("your post has been updated!", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user: # Only the current user can update their post
        abort(403) # 403 = forbidden route
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('home'))