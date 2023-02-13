from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user

@app.route("/")
def login_registration():
    return render_template("login_registration.html")

@app.route("/register", methods=["POST"])
def register():
    registration_info = {
        "first_name": request.form["fname"],
        "last_name": request.form["lname"],
        "email": request.form["em"],
        "password": request.form["pw"],
        "confirm_password": request.form["confirm_pw"]
    }
    print(f"registration_info = {registration_info}")
    if user.User.validate_registration(registration_info):
        session["id"] = user.User.insert(registration_info)
        return redirect("/wall")
    else:
        session["first_name"] = registration_info["first_name"]
        session["last_name"] = registration_info["last_name"]
        session["email"] = registration_info["email"]
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    login_info = {
        "email": request.form["email"],
        "password": request.form["pw"]
    }
    if user.User.validate_login(login_info):
        logged_in_user = user.User.get_user_by_email(login_info)
        print(f"logged_in_user = {logged_in_user}")
        session["id"] = logged_in_user.id
        print(f"session's id value = {session['id']}")
        return redirect("/wall")
    return redirect("/")
    

@app.route("/wall")
def wall():
    if "id" in session:
        return render_template("wall.html")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")