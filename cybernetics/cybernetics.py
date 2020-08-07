from .cybernetics_util import getMaxCyberNumByRole
from .cybernetics_util import rollRandomCybernetics

from util import db
from util import getFilteredQuery

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote

_cyberCollection = db.cybernetics


class CyberneticsClassificationsListApi(Resource):
    def get(self):
        return jsonify(_cyberCollection.distinct("classification"))


class CyberneticsListByClassificationApi(Resource):
    def get(self, classification):
        return jsonify(
            getFilteredQuery(
                _cyberCollection, {"classification": classification}
            )
        )


class CyberneticsListByRequirementApi(Resource):
    def get(self, requirement):
        return jsonify(
            getFilteredQuery(_cyberCollection, {"requirements": requirement})
        )


class CyberneticsGetRandomApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("role_name", type=str, default="")
        args = parser.parse_args()

        cyNum = getMaxCyberNumByRole(args["role_name"])

        return jsonify(rollRandomCybernetics(cyNum))
