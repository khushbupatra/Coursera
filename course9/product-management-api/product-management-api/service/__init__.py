from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config.py')

# Initialize database
db = SQLAlchemy(app)

# Import models after db initialization to avoid circular imports
from service.models import Product

# Import routes after app initialization
from service import routes