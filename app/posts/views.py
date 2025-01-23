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


@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    # Отримання поста за ID або повернення 404
    post = Post.query.get_or_404(id)

    # Видалення поста
    db.session.delete(post)
    db.session.commit()

    # Сповіщення про успішне видалення
    flash(f'Post "{post.title}" has been deleted successfully!', 'success')
    return redirect(url_for('.get_posts'))


@post_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    # Отримуємо пост із бази даних
    post = db.get_or_404(Post, id)
    # Ініціалізуємо форму з даними поста
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        # Оновлюємо дані поста з форми
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data

        # Зберігаємо зміни у базі даних
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))  # Повертаємося до списку постів

    return render_template('edit_post.html', form=form, post=post)