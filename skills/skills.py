from util import db
from util import getFilteredQuery
from util import distributePoints

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote

from collections import OrderedDict
from collections import deque

collection = db.skills


def getSkills():
    return getFilteredQuery(collection, {})


class SkillsListApi(Resource):
    def get(self):
        return jsonify(getFilteredQuery(collection, {}))


class PickupRandomSkillsApi(Resource):
    @staticmethod
    def buildMasterDict(skills):
        # Build masterSkills
        masterSkills = OrderedDict()
        for skill in getSkills():
            skill.update({"score": 0})
            masterSkills[skill["skill"]] = skill

        for skill in skills:
            if skill["skill"] in masterSkills:
                masterSkills[skill["skill"]]["score"] = skill["score"]
            else:
                masterSkills[skill["skill"]] = skill

        return masterSkills

    @staticmethod
    def mergeResultIntoSkill(skill, value):
        skill["score"] = value
        return skill

    @staticmethod
    def buildFinalSkillList(masterSkills, valueDeque):
        for skill in masterSkills:
            masterSkills[skill]["score"] = valueDeque.popleft()
        return [
            masterSkills[skill]
            for skill in masterSkills
            if masterSkills[skill]["score"] > 0
        ]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "skill_list", type=dict, default={}, action="append"
        )
        parser.add_argument("pickup_skill_points", type=int)
        args = parser.parse_args()
        skills = args.get("skill_list", [])

        masterSkills = PickupRandomSkillsApi.buildMasterDict(skills)

        valueList = deque(
            distributePoints(
                [masterSkills[skill]["score"] for skill in masterSkills],
                points=args["pickup_skill_points"],
            )
        )

        return jsonify(
            PickupRandomSkillsApi.buildFinalSkillList(masterSkills, valueList)
        )
