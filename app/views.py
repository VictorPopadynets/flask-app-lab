from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route('/')
def main():
    return render_template("base.html")

@app.route('/homepage') 
def home():
    agent = request.user_agent

    return render_template("homepage.html", agent=agent)

@app.errorhandler(404)
def page_not_found(error):
# Відображаємо шаблон 404.html і повертаємо статусний код 404
    return render_template('404.html'), 404
