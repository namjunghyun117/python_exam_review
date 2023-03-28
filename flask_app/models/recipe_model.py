from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app import DATABASE
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id= data['id']
        self.name= data['name']
        self.description= data['description']
        self.instructions= data['instructions']
        self.date_cooked= data['date_cooked']
        self.under_thirty= data['under_thirty']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.user_id= data['user_id']
        self.owner= None

    @classmethod
    def get_one(cls, data):
        query  = "SELECT * "
        query += "FROM recipes "
        query += "WHERE recipes.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def create_one(cls, data):
        query  = "INSERT INTO recipes(name, description, instructions, date_cooked, under_thirty, user_id)"
        query += "VALUES(%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_thirty)s, %(user_id)s );"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    @classmethod
    def get_all_with_user(cls):
        query  = "SELECT * "
        query += "FROM recipes r "
        query += "JOIN users u ON r.user_id = u.id;"

        results = connectToMySQL(DATABASE).query_db(query)
        list_of_recipes =[]

        for row in results:
            current_recipe = cls(row)
            data_for_user = {
                "id": row['u.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "created_at": row['u.created_at'],
                "updated_at": row['u.updated_at'],
                "password": row['password']
            }
            current_recipe.owner = User(data_for_user)
            list_of_recipes.append(current_recipe)
        return list_of_recipes

    @classmethod
    def get_one_with_user(cls, data):
        query  = "SELECT * "
        query += "FROM recipes r "
        query += "JOIN users u ON r.user_id = u.id "
        query += "WHERE r.id= %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        row = result[0]
        current_recipe=cls(result[0])
        data_for_user = {
            "id": row['u.id'],
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "email": row['email'],
            "created_at": row['u.created_at'],
            "updated_at": row['u.updated_at'],
            "password": row['password']
        }
        current_recipe.owner=User(data_for_user)
        return current_recipe

    @classmethod
    def delete_one(cls,data):
        query  = "DELETE FROM recipes "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def update_one(cls,data):
        query  = "UPDATE recipes "
        query += "SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under_thirty=%(under_thirty)s, user_id=%(user_id)s "
        query += "WHERE id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @staticmethod
    def validate_recipe(data):
        is_Valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters long.", "error_name")
            is_Valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters long.", "error_description")
            is_Valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.", "error_instructions")
            is_Valid = False
        if len(data['date_cooked']) == 0:
            flash("You must provide the date cooked.", "error_date_cooked")
            is_Valid = False
        if "under_thirty" not in data:
            flash("You must provide the under thirty value", "error_under_thirty")
            is_Valid = False
        return is_Valid