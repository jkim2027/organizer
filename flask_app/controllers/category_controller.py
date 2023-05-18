from flask_app import app
from flask import redirect, session, request
from flask_app.models import category

@app.route("/new-category", methods = ['POST'])
def new_category():
    data = {
        'name': request.form['name'],
        'color': request.form['color'],
        'user_id': session['user_id']
        }
    category.Category.new_category(data)
    return redirect("/dashboard")