from flask_app import app
from flask_app.models.user_model import User
from flask import render_template, session, request, redirect
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def display_login_registration_form():
    return render_template("log_reg.html")

@app.route('/user/new', methods=['POST'])
def create_user():
    # Validate the fields
    if User.validate_registration(request.form):
        #Encrypt Password
        encrypted_password = User.encrypt_password(request.form["password"], bcrypt)
        # Execute the methods holding the query
        if User.get_one_by_email({"email" : request.form['email']}, "registration") == True:
            data = {
                **request.form,
                "password" : encrypted_password
            }
            user_id = User.create_one(data)
            session['user_id'] = user_id
            session['first_name'] = request.form['first_name']
            return redirect('/recipes')
        else:
            return redirect('/')
    else:
        return redirect('/')
    
@app.route('/login', methods=['POST'])
def process_login():
    # Do the query to grab the current user's encrypted password
    current_user = User.get_one_by_email({"email": request.form["email_login"]}, "login")
    # Validate hased password against plain password
    if current_user:
        if User.validate_password(request.form["password_login"], current_user.password, bcrypt) == True:
        # Redirect to home storing user_id and first_name in session
            session['user_id'] = current_user.id
            session['first_name'] = current_user.first_name
            return redirect('/recipes')
        else:
            return redirect('/')
    else:
        return redirect('/')
    
@app.route('/logout', methods=['POST'])
def process_logout():
    session.clear()
    return redirect('/')