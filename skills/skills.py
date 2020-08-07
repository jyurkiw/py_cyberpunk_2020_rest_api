from .skills_util import getSkills
from .skills_util import addRandomPickupSkills

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote


class SkillsListApi(Resource):
    def get(self):
        return jsonify(getSkills())


class PickupRandomSkillsApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "skill_list", type=dict, default={}, action="append"
        )
        parser.add_argument("pickup_skill_points", type=int)
        args = parser.parse_args()

        return jsonify(
            addRandomPickupSkills(args.pickup_skill_points, args.skill_list)
        )
