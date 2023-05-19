from flask_app import app
from flask_app.controllers import index_controller, authentication_controller, event_controller, category_controller, task_controller, calendar_controller

app.secret_key = 'my first project'


if __name__ == "__main__":
    app.run(debug = True, port = 5003)