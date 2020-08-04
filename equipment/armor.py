from util import db
from util import getFilteredQuery

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote

collection = db.armor


class ArmorListApi(Resource):
    def get(self):
        return jsonify(getFilteredQuery(collection, {}))


class ArmorHelmetApi(Resource):
    def get(self):
        return jsonify(getFilteredQuery(collection, {"head": True}))


class ArmorJacketApi(Resource):
    def get(self):
        return jsonify(getFilteredQuery(collection, {"torso": True}))


class ArmorPantsApi(Resource):
    def get(self):
        return jsonify(getFilteredQuery(collection, {"legs": True}))


class ArmorByFilterApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("head", type=bool, default=None)
        parser.add_argument("torso", type=bool, default=None)
        parser.add_argument("arms", type=bool, default=None)
        parser.add_argument("legs", type=bool, default=None)
        parser.add_argument("soft", type=bool, default=None)
        parser.add_argument("half_vs_edged", type=bool, default=None)
        parser.add_argument("encumbrance_value", type=int, default=None)
        parser.add_argument("random_count", type=int, default=None)
        args = parser.parse_args()

        return jsonify(getFilteredQuery(collection, args))
