from .cybernetics_util import getCyberIdList, rollHumanityLoss

from util import db
from util import getFilteredQuery

from random import choice

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote

collection = db.cybernetics


class CyberneticsClassificationsListApi(Resource):
    def get(self):
        return jsonify(collection.distinct("classification"))


class CyberneticsListByClassificationApi(Resource):
    def get(self, classification):
        return jsonify(
            getFilteredQuery(collection, {"classification": classification})
        )


class CyberneticsListByRequirementApi(Resource):
    def get(self, requirement):
        return jsonify(
            getFilteredQuery(collection, {"requirements": requirement})
        )


class CyberneticsGetRandomApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("role_name", type=str, default="")
        args = parser.parse_args()

        cyNum = 6 if args["role_name"] == "Solo" else 3

        cyberList = getFilteredQuery(collection, {"random_count": cyNum})

        # Roll humanity loss
        for cyber in cyberList:
            rollHumanityLoss(cyber)

        # Handle missing pre-requisite systems
        for cyber in [c for c in cyberList if c["requirements"]]:
            cyberIds = getCyberIdList(cyberList)
            requirements = cyber["requirements"]
            intersection = set(requirements) & set(cyberIds)
            if not intersection:
                req = choice(requirements)
                requiredCyber = getFilteredQuery(collection, {"id_code": req})
                if isinstance(requiredCyber, list) and requiredCyber:
                    requiredCyber = requiredCyber[0]
                    rollHumanityLoss(requiredCyber)
                    requiredCyber["subsystems"] = [cyber]
                    cyberList.remove(cyber)
                cyberList.append(requiredCyber)
            else:
                parentId = choice(list(intersection))
                parentCyber = next(
                    (c for c in cyberList if c["id_code"] == parentId), None,
                )
                rollHumanityLoss(parentCyber)
                if not parentCyber:
                    raise Exception(
                        parentId
                        + " not found in "
                        + " | ".join([i["id_code"] for i in cyberList])
                    )
                if not parentCyber.get("subsystems", False):
                    parentCyber["subsystems"] = []
                parentCyber["subsystems"].append(cyber)
                cyberList.remove(cyber)

        return jsonify(cyberList)
