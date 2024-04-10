from flask_sqlalchemy import SQLAlchemy
from models.models import User, Game

# Initialize the SQLAlchemy extension
db = SQLAlchemy()

# Configure the database connection details
def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3rQ1eq0z1TLN@localhost:3306/game_db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
