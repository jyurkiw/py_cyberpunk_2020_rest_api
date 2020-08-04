from util import db
from util import getFilteredQuery

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote

collection = db.weapons


class WeaponsListApi(Resource):
    def get(self):
        return jsonify(getFilteredQuery(collection, {}))


class WeaponCategoriesListApi(Resource):
    def get(self):
        return jsonify(collection.distinct("category"))


class WeaponsByAvailabilityApi(Resource):
    def get(self, availability):
        return jsonify(
            getFilteredQuery(collection, {"availability": availability})
        )


class WeaponsByCategoryApi(Resource):
    def get(self, category):
        return jsonify(
            getFilteredQuery(collection, {"category": unquote(category)})
        )


class WeaponsByConcealabilityApi(Resource):
    def get(self, concealability):
        return jsonify(
            getFilteredQuery(collection, {"concealability": concealability})
        )


class WeaponsByFilterApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("availability", type=str, default=None)
        parser.add_argument("category", type=str, default=None)
        parser.add_argument("concealability", type=str, default=None)
        parser.add_argument("reliability", type=str, default=None)
        parser.add_argument("type", type=str, default=None)
        parser.add_argument("ammo_type", type=str, default=None)
        parser.add_argument("random_count", type=int, default=None)
        args = parser.parse_args()

        return jsonify(getFilteredQuery(collection, args))
