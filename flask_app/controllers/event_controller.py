from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import event, category

@app.route("/new-event")
def new_event():
    all_categories = category.Category.all_categories()
    return render_template("create/create_event.html", all_categories=all_categories)

@app.route("/new-event", methods = ['POST'])
def create_event():
    if not event.Event.validate_event(request.form):
        return redirect("/new-event")
    
    selected_category = request.form['category_id']
    if selected_category == 'other':
        category_data = {
            'name': request.form['category'],
            'color': request.form['color'],
            'user_id': session['user_id']
        }
    new_category = category.Category.new_category(category_data)
    selected_category = new_category
    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'time': request.form['time'],
        'location': request.form['location'],
        'notes': request.form['notes'],
        'user_id': session['user_id'],
        'category_id': selected_category   
        }
    event.Event.create_event(data)
    return redirect("/dashboard")

@app.route("/delete/event/<int:event_id>")
def delete_event(event_id):
    event.Event.delete_event(event_id)
    return redirect("/dashboard")

@app.route("/edit/event/<int:event_id>")
def edit_event(event_id):
    one_event = event.Event.show_one_event(event_id)
    all_categories = category.Category.all_categories()
    return render_template("edit/edit_event.html", one_event=one_event, all_categories=all_categories)

@app.route("/edit/event/<int:event_id>", methods = ['POST'])
def update_event(event_id):
    if not event.Event.validate_event(request.form):
        return redirect(f"/edit/event/{event_id}")
    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'time': request.form['time'],
        'location': request.form['location'],
        'notes': request.form['notes'],
        'category_id': request.form['category_id'],
        'event_id': event_id,
    }
    event.Event.edit_event(data)
    return redirect("/dashboard")

@app.route("/view/event/<int:event_id>")
def view_one_event(event_id):
    one_event = event.Event.show_one_event(event_id)
    return render_template("detail/view_event.html", one_event=one_event)
