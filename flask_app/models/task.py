from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import category
from flask import flash


class Task:
    DB = 'organizer'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.deadline = db_data['deadline']
        self.reoccurring = db_data['reoccurring']
        self.reoccurring_freq = db_data['reoccurring_freq']
        self.reoccurring_type = db_data['reoccurring_type']
        self.notes = db_data['notes']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.category_id = db_data['category_id']
        self.category = None


    @classmethod
    def create_task(cls, data):
        query = "INSERT INTO tasks (name, deadline, reoccurring, reoccurring_freq, reoccurring_type, notes, category_id, user_id, created_at, updated_at) VALUES (%(name)s, %(deadline)s, %(reoccurring)s, %(reoccurring_freq)s, %(reoccurring_type)s, %(notes)s, %(category_id)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
        
    # @classmethod 
    # def all_tasks(cls):
    #     query = "SELECT * FROM tasks"
    #     results = connectToMySQL(cls.DB).query_db(query)
    #     all_tasks = []
    #     for each_task in results:
    #         all_tasks.append(cls(each_task))
    #     return all_tasks

    @classmethod 
    def all_tasks(cls):
        query = "SELECT * FROM tasks JOIN categories ON categories.id=tasks.category_id"
        results = connectToMySQL(cls.DB).query_db(query)
        all_tasks = []
        for task in results:
            each_task = cls(task)
            each_category = category.Category({
                'id' : task['id'],
                'name' : task['categories.name'],
                'color' : task['color'],
                'created_at' : task['categories.created_at'],
                'updated_at' : task['categories.updated_at'],
                'user_id' : task['categories.user_id']
            })
            each_task.category = each_category
            all_tasks.append(each_task)
        return all_tasks
    
    @classmethod
    def delete_task(cls, task_id):
        data = {'id': task_id}
        query = "DELETE FROM tasks WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def edit_task(cls, data):
        query = "UPDATE tasks SET name = %(name)s, deadline = %(deadline)s, reoccurring = %(reoccurring)s, reoccurring_freq = %(reoccurring_freq)s, reoccurring_type = %(reoccurring_type)s, notes = %(notes)s, category_id = %(category_id)s WHERE id=%(task_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def show_one_task(cls, task_id):
        query = "SELECT * FROM tasks WHERE id=%(id)s"
        data = {'id': task_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @staticmethod
    def validate_task(task):
        is_valid = True
        if len(task['name']) <= 0:
            flash("Task must have a name.","task")
            is_valid = False
        if task['category_id'] == 'none':
            flash("Please choose a category.","task")
            is_valid = False
        if len(task['deadline']) <= 0:
            flash("Date must be given.","task")
            is_valid = False
        return is_valid