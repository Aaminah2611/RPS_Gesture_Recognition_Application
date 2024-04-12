from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import User, Game  # Import your models here
