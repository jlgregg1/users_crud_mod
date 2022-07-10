from flask_app import app #must import app to run it
from flask_app.controllers import users #always import all controller files

if __name__ == "__main__":
    app.run(debug=True)
