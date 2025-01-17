from . import bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta, datetime

DEMO_USERNAME = "admin"
DEMO_PASSWORD = "password123"

@bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("hi.html",
                           name=name, age=age)

@bp.route("/admin")
def admin():
    to_url = url_for("user_name.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Перевірка даних для автентифікації
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("user_name.get_profile"))
        else:
            flash("Неправильний логін або пароль.", "danger")
            return redirect(url_for("user_name.login"))

    return render_template("login.html")



# Route для виходу
@bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("user_name.login"))

@bp.route("/set_color/<string:color>")
def set_color(color):
    if "username" in session:
        response = make_response(redirect(url_for("user_name.get_profile")))
        response.set_cookie("color_scheme", color, max_age=30*24*60*60)
        flash(f"Колірна схема змінена на '{color}'", "info")
        return response
    flash("Вам потрібно увійти, щоб змінити кольорову схему.", "danger")
    return redirect(url_for("user_name.login"))



@bp.route("/profile")
def get_profile():
    if "username" in session:
        username = session["username"]
        cookies = request.cookies  # Отримання всіх кукі
        return render_template("profile.html", username=username, cookies=cookies)
    flash("Будь ласка, увійдіть, щоб переглянути профіль.", "danger")
    return redirect(url_for("user_name.login"))

@bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "username" in session:
        key = request.form.get("key")
        value = request.form.get("value")
        expiry = int(request.form.get("expiry"))

        response = make_response(redirect(url_for("user_name.get_profile")))
        response.set_cookie(key, value, max_age=expiry)
        flash(f"Кука '{key}' успішно додана!", "success")
        return response
    flash("Вам потрібно увійти, щоб керувати кукі.", "danger")
    return redirect(url_for("user_name.login"))

@bp.route("/delete_cookie_by_key", methods=["POST"])
def delete_cookie_by_key():
    if "username" in session:
        key = request.form.get("cookie_key")
        response = make_response(redirect(url_for("user_name.get_profile")))
        response.set_cookie(key, "", expires=0)
        flash(f"Кука '{key}' успішно видалена!", "info")
        return response
    flash("Вам потрібно увійти, щоб видалити кукі.", "danger")
    return redirect(url_for("user_name.login"))

@bp.route("/delete_all_cookies", methods=["POST"])
def delete_all_cookies():
    if "username" in session:
        response = make_response(redirect(url_for("user_name.get_profile")))
        for key in request.cookies.keys():
            response.set_cookie(key, "", expires=0)
        flash("Усі кукі успішно видалені!", "info")
        return response
    flash("Вам потрібно увійти, щоб керувати кукі.", "danger")
    return redirect(url_for("user_name.login"))
