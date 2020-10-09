# schemas.py
# pylint: disable=missing-docstring

from wsgi import ma
from models import Game


class GameSchema(ma.Schema):
    class Meta:
        model = Game
        fields = ('id', 'name', 'description') # These are the fields we want in the JSON!


one_game_schema = GameSchema()
many_game_schema = GameSchema(many=True)
