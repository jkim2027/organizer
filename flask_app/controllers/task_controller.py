from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import task, category

@app.route("/new-task")
def new_task():
    # all_categories = category.Category.all_categories()
    data = {'id': session['user_id']}
    all_categories = category.Category.all_categories_with_user(data)
    return render_template("create/create_task.html", all_categories=all_categories)

@app.route("/new-task", methods = ['POST'])
def create_task():
    if not task.Task.validate_task(request.form):
        return redirect("/new-task")
    selected_category = request.form['category_id']
    if selected_category == 'other':
        category_data = {
            'name': request.form['category'],
            'color': request.form['color'],
            'user_id': session['user_id']
        }
        new_category = category.Category.new_category(category_data)
        selected_category = new_category
    reoc_freq = request.form["reoccurring_freq"]
    data = {
        'name': request.form['name'],
        'deadline': request.form['deadline'],
        'reoccurring': request.form['reoccurring'],
        'reoccurring_freq': reoc_freq if reoc_freq != "" else None,
        'reoccurring_type': request.form['reoccurring_type'],
        'notes': request.form['notes'],
        'user_id': session['user_id'],
        'category_id': selected_category
        }
    task.Task.create_task(data)
    return redirect("/dashboard")

@app.route("/delete/task/<int:task_id>")
def delete_task(task_id):
    task.Task.delete_task(task_id)
    return redirect("/dashboard")

@app.route("/edit/task/<int:task_id>")
def edit_task(task_id):
    data = {'id': session['user_id']}
    one_task = task.Task.show_one_task(task_id)
    # all_categories = category.Category.all_categories()
    all_categories = category.Category.all_categories_with_user(data)
    return render_template("edit/edit_task.html", one_task=one_task, all_categories=all_categories)

@app.route("/edit/task/<int:task_id>", methods = ['POST'])
def update_task(task_id):
    if not task.Task.validate_task(request.form):
        return redirect(f"/edit/task/{task_id}")
    selected_category = request.form['category_id']
    if selected_category == 'other':
        category_data = {
            'name': request.form['category'],
            'color': request.form['color'],
            'user_id': session['user_id']
        }
        new_category = category.Category.new_category(category_data)
        selected_category = new_category
    reoc_freq = request.form["reoccurring_freq"]
    data = {
        'name': request.form['name'],
        'deadline': request.form['deadline'],
        'reoccurring': request.form['reoccurring'],
        'reoccurring_freq': reoc_freq if reoc_freq != "" else None,
        'reoccurring_type': request.form['reoccurring_type'],
        'notes': request.form['notes'],
        'category_id': selected_category,
        'task_id': task_id
    }
    task.Task.edit_task(data)
    return redirect("/dashboard")

@app.route("/view/task/<int:task_id>")
def view_one_task(task_id):
    one_task = task.Task.show_one_task(task_id)
    return render_template("detail/view_task.html", one_task=one_task)
