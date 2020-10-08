from wsgi import db
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


class JGamePlatform(db.Model):
    __tablename__ = "j_games_platforms"
    game_id = db.Column('game_id', db.Integer, ForeignKey('games.id'), primary_key=True)
    platform_id = db.Column('platform_id', db.Integer, ForeignKey('platforms.id'), primary_key=True)
    games = db.relationship("Game", backref=backref("j_games_platforms"))
    platforms = db.relationship("Platform", backref=backref("j_games_platforms"))

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    release_date = db.Column(db.Date())
    platforms = db.relationship("Platform", secondary="j_games_platforms", back_populates="games")
    publisher_id = db.Column(db.Integer, ForeignKey('publishers.id'))
    publisher = db.relationship("Publisher", back_populates="games")

class Platform(db.Model):
    __tablename__ = "platforms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    released = db.Column(db.String())
    games = db.relationship('Game', secondary="j_games_platforms", back_populates="platforms")
    publisher_id = db.Column(db.Integer, ForeignKey('publishers.id'))
    publisher = db.relationship('Publisher', back_populates="platforms")


class Publisher(db.Model):
    __tablename__ = "publishers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    headquarters = db.Column(db.String())
    established = db.Column(db.String())
    games = db.relationship('Game', back_populates="publisher")
    platforms = db.relationship('Platform', back_populates="publisher")

    def __repr__(self):
        return f'<id {self.id}>'
