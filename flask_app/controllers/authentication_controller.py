from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import redirect, request, session, flash
from flask_app.models import user

@app.route("/register", methods = ['POST'])
def register_user():
    if not user.User.validate_user(request.form):
        return redirect("/register")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = user.User.register_user(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route("/login", methods = ['POST'])
def login_user():
    data = {'email': request.form['email']}
    user_in_db = user.User.get_by_email(data)
    if len(request.form['email']) <= 0 or len(request.form['password']) <= 0:
        flash("All fields required.", 'login')
        return redirect("/login")
    if not user_in_db:
        flash("Invalid email address.", 'login')
        return redirect ("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid password.", 'login')
        return redirect("/login")
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")