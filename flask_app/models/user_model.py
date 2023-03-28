from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_by_email(cls, data, option):
        query  = "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s;"

        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) > 0:
            if option == "registration":
                flash("Email already in use, please select another one.", "email_error")
                return False
            if option == "login":
                return cls(result[0])
        else:
            if option =="registration":
                return True
            if option =="login":
                flash("Wong credentials", "password_login_error")
                return False

    @classmethod
    def create_one(cls, data):
        query  = "INSERT INTO users(first_name, last_name, email, password )"
        query += "VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters long.', 'first_name_error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters long.', 'last_name_error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address.', 'email_error')
            is_valid = False
        if data['password'] != data['password_confirmation']:
            flash('Password and password confirmation do not match.', 'password_error')
            is_valid = False
        return is_valid
    
    @staticmethod
    def encrypt_password(pwd, bcrypt):
        return bcrypt.generate_password_hash(pwd)
    
    @staticmethod
    def validate_password(pwd, encrypted_pwd, bcrypt):
        if not bcrypt.check_password_hash(encrypted_pwd, pwd):
            flash("Wrong credentials", "password_login_error")
            return False
        else:
            return True