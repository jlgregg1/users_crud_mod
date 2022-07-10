from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at'] #make sure to include so that it can be referenced and displayed
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
    # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('user_schema').query_db(query, data)

    @classmethod
    def view_all(cls):
        query = "select * FROM users"
        results = connectToMySQL('user_schema').query_db(query)
        if len(results) == 0: #returns empty list if no users in DB
            return []
        else:
            user_objects = [] #make list of users that can be referenced in the HTML file for display
            for this_user_dictionary in results:
                new_user_object = cls(this_user_dictionary) #makes it possible to use dot syntax to reference the class properties from HTML doc
                user_objects.append(new_user_object)
            return user_objects
            #this return will be passed into the "/users" route to define the list of all users, which is then passed into HTML as variable "all_users" and then iterated through using a for loop

    @classmethod
    def view_one(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;" #pass in id as variable
        results = connectToMySQL('user_schema').query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0]) #results is a list, want to return the first result (should only return one result if that id is present)
    
    @classmethod
    def edit_one(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;" #must specify WHERE in order to update correct row
        return connectToMySQL('user_schema').query_db(query, data) #no additional needed, as it does not return anything, just updates database

    @classmethod
    def delete_from_db(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('user_schema').query_db(query, data)
