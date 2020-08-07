from .characters_util import getRandomSingleCharacter

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse


class CharactersRandomSingleApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("character_points", type=int, default=60)
        parser.add_argument("career_skill_points", type=int, default=40)
        parser.add_argument("role_name", type=str, default=None)
        parser.add_argument(
            "lifepath_restrictions", type=str, default="complete"
        )
        args = parser.parse_args()

        return jsonify(getRandomSingleCharacter(**args))
