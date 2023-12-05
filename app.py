import os
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from util.route import main_routes  # Import the routes from route.py
from util.models import db, HR, User
from flask_login import LoginManager

# Basic configuration
app = Flask(__name__)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/smart-job-search.db')
app.config['SECRET_KEY'] = '10086'
db.init_app(app)

# Import the routes
app.register_blueprint(main_routes)

# Main routine
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)