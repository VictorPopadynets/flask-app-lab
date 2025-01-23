from flask import request, render_template
from . import create_app

def register_routes(app):
    @app.route('/')
    def main():
        return render_template("base.html")

    @app.route('/homepage')
    def home():
        agent = request.user_agent
        return render_template("home.html", agent=agent)

    @app.errorhandler(404)
    def page_not_found(error):
        # Відображаємо шаблон 404.html і повертаємо статусний код 404
        return render_template('404.html'), 404

