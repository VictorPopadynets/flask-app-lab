import json
from . import post_bp
from flask import render_template, abort, flash, redirect, url_for
from .forms import PostForm



@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content,
            "category": form.category.data,
            "author": form.author.data,
            "is_active": True,
            "publication_date": "2024-11-05"
        }

        posts.append(new_post)
        save_posts(posts)

        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('.get_posts'))

    return render_template("add_post.html", form=form)

@post_bp.route('/') 
def get_posts():
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = next((p for p in posts if p["id"] == id), None)
    if not post:
        abort(404)
    return render_template("detail_post.html", post=post)
