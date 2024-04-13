from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    participants = db.relationship('Participant', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')

    user_1 = db.relationship('User', foreign_keys=[user_id_1], backref='games_as_user_1')
    user_2 = db.relationship('User', foreign_keys=[user_id_2], backref='games_as_user_2', remote_side=[id])

    participants = db.relationship('Participant', backref='game', lazy=True)

    def __repr__(self):
        return f"Game(id={self.id}, user_id_1={self.user_id_1}, user_id_2={self.user_id_2}, started_at={self.started_at}, status={self.status})"


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gesture = db.Column(db.String(50))
    player_number = db.Column(db.Integer)

    def __repr__(self):
        return f"Participant(id={self.id}, game_id={self.game_id}, user_id={self.user_id}, gesture={self.gesture}, player_number={self.player_number})"
