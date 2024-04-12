from flask_sqlalchemy import SQLAlchemy
from models import User, Game  # Import your models here

db = SQLAlchemy()

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3rQ1eq0z1TLN@localhost:3306/game_db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
