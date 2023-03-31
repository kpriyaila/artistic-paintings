from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Painting:
    db = "userpaintings"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']        
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title,description,price, users_id) VALUES(%(title)s,%(description)s,%(price)s,%(users_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):        
        query = "SELECT paintings.id, title, description, price, paintings.created_at, paintings.updated_at, paintings.users_id, first_name FROM userpaintings.paintings inner join userpaintings.users on paintings.users_id = userpaintings.users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        paintings = []
        for row in results:
            paintings.append( cls(row))
        return paintings

    @classmethod
    def get_all_with_userinfo(cls):
        query = "SELECT paintings.id, title, description, price, paintings.created_at, paintings.updated_at, paintings.users_id, first_name, last_name FROM userpaintings.paintings left join userpaintings.users on paintings.users_id = userpaintings.users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        paintings = []
        for row in results:
            paintings.append( cls(row))
        return paintings
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_by_id(cls,data):
        query = "SELECT paintings.id, title, description, price, paintings.created_at, paintings.updated_at, paintings.users_id, first_name, last_name FROM userpaintings.paintings inner join userpaintings.users on paintings.users_id = userpaintings.users.id AND userpaintings.paintings.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, users_id=%(users_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_show(paintings):
        is_valid = True
        if len(paintings['title']) < 3:
            flash("Title must be at least 3 characters","register")
            is_valid= False        
        if len(paintings['description']) < 8:
            flash("Description must be at least 8 characters","register")
            is_valid= False
        if paintings['price'] == '':
            is_valid= False
            flash("Please enter a valid price","register")
        return is_valid