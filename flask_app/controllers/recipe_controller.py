from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask import render_template, session, request, redirect

@app.route('/recipes', methods=['GET'])
def get_recipes():
    if 'user_id' in session:
        list_of_recipes = Recipe.get_all_with_user()
        return render_template("recipes.html", list_of_recipes=list_of_recipes)
    else:
        return redirect('/')
    
@app.route('/recipes/new', methods=['GET'])
def display_recipe_form():
    if 'user_id' in session:
        return render_template("recipe_form.html")
    else:
        return redirect('/')

@app.route('/recipe/new', methods=['POST'])
def created_recipe():
    if Recipe.validate_recipe(request.form) == True:
        data = {
            **request.form,
            "user_id": session['user_id']
        }
        Recipe.create_one(data)
        return redirect('/recipes')
    else:
        return redirect('/recipes/new')

@app.route('/recipe/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    Recipe.delete_one({"id":id})
    return redirect('/recipes')

@app.route('/recipes/edit/<int:id>', methods=['GET'])
def display_update_recipe_form(id):
    if 'user_id' in session:
        current_recipe = Recipe.get_one({"id": id})
        return render_template("update_recipe_form.html", current_recipe=current_recipe)
    else:
        return redirect('/')

@app.route('/recipe/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if Recipe.validate_recipe(request.form) == True:
        data = {
            **request.form,
            "id" : id,
            "user_id": session['user_id']
        }
        Recipe.update_one(data)
        return redirect('/recipes')
    else:
        return redirect(f'/recipes/edit/{id}')
    
@app.route('/recipe/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    if 'user_id' in session:
        current_recipe = Recipe.get_one_with_user({"id":id})
        return render_template("recipe.html", current_recipe=current_recipe)
    else: 
        return redirect('/')