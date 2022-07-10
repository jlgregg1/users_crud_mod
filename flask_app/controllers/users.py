from flask import Flask, render_template, session, request, redirect
from flask_app import app
from flask_app.models.user import User

#visible
@app.route("/")
def index():
    return redirect("/users")

@app.route("/users")
def view_user():
    return render_template("read_all.html", all_users = User.view_all())

@app.route("/users/new")
def new_user():
    return render_template("create.html")

@app.route("/users/<int:id>/edit")
def edit(id):
    data = {
        "id": id #need ID for the query. This id was passed into the function from the URL in the route
    }
    return render_template("edit.html", one_user = User.view_one(data))

@app.route("/users/<int:id>/view_one")
def view_one(id):
    data = {
        "id": id #need ID for the query. This id was passed into the function from the URL in the route
    }
    return render_template("read_one.html", one_user = User.view_one(data))

#hidden
@app.route("/create_user_in_db", methods = ['POST'])
def create_user_in_db():
# First we make a data dictionary from our request.form coming from our template.
# The keys in data need to line up exactly with the variables in the query string (see user doc).
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email" : request.form["email"],
        }
    return redirect(f'/users/{User.save(data)}/view_one') #the return of the User.save function is the id of the created item in the db (insert into queries return the most recently-created ID. This can be passed into the URL as a variable using f string)

@app.route("/users/<int:id>/edit_user_in_db", methods = ["POST"])
def edit_user_in_db(id):
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "id": id #need this to properly update this specific user using query
    }
    User.edit_one(data)
    return redirect(f'/users/{id}/view_one') #can use f string here becuase no risk of SQL injection

@app.route("/users/<int:id>/delete")
def delete_user(id):
    data = {
        "id": id #need ID for the query. This id was passed into the function from the URL in the route
    }
    User.delete_from_db(data)
    return redirect("/users")