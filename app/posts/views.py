from flask import render_template, flash, redirect, url_for
from . import post_bp
from .forms import PostForm
from .models import Post
from app import db

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Creating a new post from the form data
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=form.author.data,
            is_active=True  # Ensure the post is active by default
        )

        # Adding to the database
        db.session.add(new_post)
        db.session.commit()
        flash(f'Post "{new_post.title}" added successfully!', 'success')
        return redirect(url_for('.get_posts'))  # Redirect to list all posts

    return render_template("add_post.html", form=form)


@post_bp.route('/')
def get_posts():
    # Fetch active posts from the database, ordered by most recent
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    # Fetch the post by ID, or return 404 if not found
    post = Post.query.get_or_404(id)
    return render_template("detail_post.html", post=post)
