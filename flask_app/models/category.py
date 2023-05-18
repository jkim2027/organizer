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
        # self.tasks = []
        # self.events = []


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
    
    # @classmethod
    # def get_categories_with_events(cls):
    #     query = "SELECT * FROM categories JOIN events ON categories.id=events.category_id"
    #     results = connectToMySQL(cls.DB).query_db(query)
    #     all_categories = []
    #     for category in results:
    #         each_category = cls({
    #             'id' : category['id'],
    #             'name' : category['name'],
    #             'color' : category['color'],
    #             'created_at' : category['created_at'],
    #             'updated_at' : category['updated_at'],
    #             'user_id' : category['user_id']
    #         })
    #         each_event = event.Event({
    #             'id' : category['events.id'],
    #             'name' : category['events.name'],
    #             'date' : category['date'],
    #             'time' : category['time'],
    #             'location' : category['location'],
    #             'notes' : category['notes'],
    #             'created_at' : category['events.created_at'],
    #             'updated_at' : category['events.updated_at'],
    #             'user_id' : category['events.user_id'],
    #             'category_id' : category['category_id']
    #         })
    #         each_category.events = each_event
    #         all_categories.append(each_category)
    #     return all_categories