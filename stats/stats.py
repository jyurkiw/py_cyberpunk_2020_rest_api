from .stats_util import getDefaultStatBlock
from .stats_util import finalizeStatBlock

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse


class StatBlockApi(Resource):
    def get(self, points):
        return jsonify(getDefaultStatBlock(points))


class StatBlockFinalizeApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("attractiveness", type=int)
        parser.add_argument("body", type=int)
        parser.add_argument("cool", type=int)
        parser.add_argument("empathy", type=int)
        parser.add_argument("encumbrance_value", type=int)
        parser.add_argument("humanity", type=int)
        parser.add_argument("intelligence", type=int)
        parser.add_argument("leap", type=int)
        parser.add_argument("lift", type=int)
        parser.add_argument("luck", type=int)
        parser.add_argument("movement_allowance", type=int)
        parser.add_argument("reflex", type=int)
        parser.add_argument("reputation", type=int)
        parser.add_argument("run", type=int)
        parser.add_argument("technical", type=int)
        args = parser.parse_args()

        return jsonify(finalizeStatBlock(args))
