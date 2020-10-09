# wsgi.py
# pylint: disable=missing-docstring

from config import Config
from flask import Flask, abort, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # NEW LINE (Order is important here!)


import pandas as pd
import requests


BASE_URL = '/api/v1'
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

ma = Marshmallow(app)
from models import Game, Publisher, Platform, JGamePlatform
from schemas import many_game_schema, one_game_schema
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from db_load_data import db_initiate_data
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(Game, db.session))
admin.add_view(ModelView(Publisher, db.session))
admin.add_view(ModelView(Platform, db.session))
admin.add_view(ModelView(JGamePlatform, db.session))
db_initiate_data(db)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/calendar')
def calendar():
    r = requests.get('http://www.gameblog.fr/sorties.php?mois=2020-10')
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    df = df_list[1]
    return df.to_string()


@app.route('/publisher')
def publisher():
    r = requests.get('https://en.wikipedia.org/wiki/List_of_video_game_publishers')
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    df = df_list[1]
    return df.to_string()


@app.route(f'{BASE_URL}/games', methods=['GET'])
def get_many_game():
    games = db.session.query(Game).all() # SQLAlchemy request => 'SELECT * FROM games'
    return many_game_schema.jsonify(games), 200


@app.route(f'{BASE_URL}/games', methods=['POST'])
def create_one_game():
    content = request.json
    name = content.get('name', None)
    description = content.get('description', '')
    if name is None:
        return {}, 404
    new_game = Game(name=name, description=description)
    db.session.add(new_game)
    db.session.commit()
    return one_game_schema.jsonify(new_game), 201


@app.route(f'{BASE_URL}/games/<int:id>', methods=['GET'])
def get_one_game(id):
    game = db.session.query(Game).get(id)
    return one_game_schema.jsonify(game), 200


@app.route(f'{BASE_URL}/games/<int:id>', methods=['DELETE'])
def delete_one_game(id):
    db.session.query(Game).filter_by(id=id).delete()
    db.session.commit()
    return {}, 204


@app.route(f'{BASE_URL}/games/<int:id>', methods=['PATCH'])
def update_one_game(id):
    game = db.session.query(Game).get(id)
    if game is None:
        return {}, 404
    content = request.json
    name = content.get('name', None)
    description = content.get('description', None)
    if name is not None and name != '':
        game.name = name
    if description is not None and description != '':
        game.description = description
    db.session.add(game)
    db.session.commit()
    return one_game_schema.jsonify(game), 201
