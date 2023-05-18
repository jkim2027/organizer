from flask_app.config.mysqlconnection import connectToMySQL
import datetime
from flask_app.models import category
from flask import flash

class Event:
    DB = 'organizer'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.date = db_data['date']
        self.time = db_data['time']
        self.location = db_data['location']
        self.notes = db_data['notes']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.category_id = db_data['category_id']
        self.category = None


    @classmethod
    def create_event(cls, data):
        query = "INSERT INTO events (name, date, time, location, notes, category_id, user_id, created_at, updated_at) VALUES (%(name)s, %(date)s, %(time)s, %(location)s, %(notes)s, %(category_id)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod 
    def all_events(cls):
        query = "SELECT * FROM events JOIN categories ON categories.id=events.category_id"
        results = connectToMySQL(cls.DB).query_db(query)
        all_events = []
        for event in results:
            each_event = cls(event)
            each_category = category.Category({
                'id' : event['id'],
                'name' : event['categories.name'],
                'color' : event['color'],
                'created_at' : event['categories.created_at'],
                'updated_at' : event['categories.updated_at'],
                'user_id' : event['categories.user_id']
            })
            each_event.category = each_category
            all_events.append(each_event)
        return all_events
    
    @classmethod 
    def all_events_with_user(cls, user_id):
        query = "SELECT * FROM events JOIN categories ON categories.id=events.category_id WHERE events.user_id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, user_id)
        all_events = []
        for event in results:
            each_event = cls(event)
            each_category = category.Category({
                'id' : event['id'],
                'name' : event['categories.name'],
                'color' : event['color'],
                'created_at' : event['categories.created_at'],
                'updated_at' : event['categories.updated_at'],
                'user_id' : event['categories.user_id']
            })
            each_event.category = each_category
            all_events.append(each_event)
        return all_events
    
    @classmethod
    def delete_event(cls, event_id):
        data = {'id': event_id}
        query = "DELETE FROM events WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def edit_event(cls, data):
        query = "UPDATE events SET name = %(name)s, date = %(date)s, time = %(time)s, location = %(location)s, notes = %(notes)s, category_id = %(category_id)s WHERE id=%(event_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def show_one_event(cls, event_id):
        query = "SELECT * FROM events WHERE id=%(id)s"
        data = {'id': event_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def show_time(cls, event_id):
        query = "SELECT TIME_FORMAT(time, '%h:%i %p') FROM events WHERE id=%(id)s"
        data = {'id': event_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    def getFormattedTime(self):
        time_string = str(self.time) 
        result_datetime = datetime.datetime.strptime(time_string, '%H:%M:%S')
        formated_time = result_datetime.strftime('%I:%M %p')
        return formated_time

    
    @staticmethod
    def validate_event(event):
        is_valid = True
        if len(event['name']) <= 0:
            flash("Event must be given a name.","event")
            is_valid = False
        if event['category_id'] == 'none':
            flash("Please choose a category.","event")
            is_valid = False
        if len(event['date']) <= 0:
            flash("Date must be given.","event")
            is_valid = False
        if len(event['time']) <= 0:
            flash("Time must be given.", "event")
            is_valid = False
        if len(event['location']) <= 0:
            flash("Location must be given.", "event")
            is_valid = False
        return is_valid