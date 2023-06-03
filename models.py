from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import pbkdf2_sha256

db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    credits = db.Column(db.Integer, default=0)
    games = db.relationship('Game', backref='player', lazy=True)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)
    
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    game_time = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.String(5), nullable=False)
    session = db.Column(db.Integer, nullable=False)
