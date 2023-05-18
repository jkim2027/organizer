from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import event, task

class Category:
    DB = 'organizer'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.color = db_data['color']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.tasks = []
        self.events = []


    @classmethod
    def new_category(cls, data):
        query = "INSERT INTO categories (name, color, user_id, created_at, updated_at) VALUES (%(name)s, %(color)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def all_categories(cls):
        query = "SELECT * FROM categories"
        results = connectToMySQL(cls.DB).query_db(query)
        all_categories = []
        for each_category in results:
            all_categories.append(cls(each_category))
        return all_categories
    
    @classmethod
    def all_categories_with_user(cls, user_id):
        query = "SELECT * FROM categories WHERE user_id = %(id)s"
        # data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query,user_id)
        all_categories = []
        for each_category in results:
            all_categories.append(cls(each_category))
        return all_categories
    
    # @classmethod
    # def get_categories_with_events_and_tasks(cls, user_id):
    #     query = "SELECT * FROM categories JOIN events ON categories.id=events.category_id JOIN tasks ON categories.id = tasks.category_id WHERE categories.user_id = %(id)s"
    #     results = connectToMySQL(cls.DB).query_db(query, user_id)
    #     all_categories = []
    #     for each_category in results:
    #         one_category = cls(each_category)
    #         each_event = event.Event({
    #             'id' : each_category['events.id'],
    #             'name' : each_category['events.name'],
    #             'date' : each_category['date'],
    #             'time' : each_category['time'],
    #             'location' : each_category['location'],
    #             'notes' : each_category['notes'],
    #             'created_at' : each_category['events.created_at'],
    #             'updated_at' : each_category['events.updated_at'],
    #             'user_id' : each_category['events.user_id'],
    #             'category_id' : each_category['category_id']
    #         })
    #         each_task = task.Task({
    #             'id' : each_category['tasks.id'],
    #             'name' : each_category['tasks.name'],
    #             'deadline' : each_category['deadline'],
    #             'reoccurring' : each_category['reoccurring'],
    #             'reoccurring_freq' : each_category['reoccurring_freq'],
    #             'reoccurring_type' : each_category['reoccurring_type'],
    #             'notes' : each_category['tasks.notes'],
    #             'created_at' : each_category['tasks.created_at'],
    #             'updated_at' : each_category['tasks.updated_at'],
    #             'category_id' : each_category['tasks.category_id'],
    #             'user_id' : each_category['tasks.user_id']
    #         })
    #         one_category.events.append(each_event)
    #         one_category.tasks.append(each_task)
    #         all_categories.append(one_category)
    #     return all_categories