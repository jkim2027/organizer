from flask_app import app
from flask import render_template, redirect, session
from flask_app.models import category, event, task, user
import datetime

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    else:
        data = {'id': session['user_id']}
        one_user = user.User.get_by_id(data)
        # all_categories = category.Category.all_categories()
        all_categories = category.Category.all_categories_with_user(data)
        # all_events = event.Event.all_events()
        all_events = event.Event.all_events_with_user(data)
        # all_tasks = task.Task.all_tasks()
        all_tasks = task.Task.all_tasks_with_user(data)
        date = datetime.datetime.now()
    return render_template("dashboard.html", all_categories=all_categories, all_events=all_events, date = date, all_tasks=all_tasks, user=one_user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/cancel")
def cancel():
    return redirect("/dashboard")

