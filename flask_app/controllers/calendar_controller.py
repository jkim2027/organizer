from flask_app import app
from flask import render_template
import calendar
import locale
from datetime import datetime, timedelta
from flask_app.models import event, task


@app.route("/calendar")
def my_calendar():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    month_name = current_date.strftime('%B')

    # Create a calendar object
    cal = calendar.monthcalendar(year, month)
    print("cal", cal)

    all_events = event.Event.all_events()
    events = []
    for one_event in all_events:
        event_dict = {
            "label": one_event.name,
            "date": one_event.date,
            "color": one_event.category.color,
            "id": one_event.id
        }
        events.append(event_dict)

    all_tasks = task.Task.all_tasks()
    tasks = []
    for one_task in all_tasks:
        task_dict = {
            "label": one_task.name,
            "date": one_task.deadline,
            "color": one_task.category.color,
            "id": one_task.id
        }
        tasks.append(task_dict)

    return render_template('detail/calendar.html', cal=cal, events=events, tasks = tasks, month_name=month_name)
