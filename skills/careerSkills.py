from .skills_util import getCareerSkillsForRole
from .skills_util import getRoleNames
from .skills_util import getRandomSkillsByRole
from .skills_util import getRandomSkillsAndRole
from .skills_util import getRandomSkillsAndRoleWithPickups

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote


class CareersListApi(Resource):
    def get(self):
        return jsonify(getRoleNames())


class CareerSkillsForRoleApi(Resource):
    def get(self, role_name):
        return jsonify(getCareerSkillsForRole(role_name))


class CareerRandomSkillsByRoleApi(Resource):
    def get(self, role_name, points=40):
        return jsonify(getRandomSkillsByRole(role_name, points))


class CareerRandomSkillsAndRoleApi(Resource):
    def get(self, points=40):
        return jsonify(getRandomSkillsAndRole(points))


class SkillsAndRoleRandomCompleteApi(Resource):
    def get(self, career_skill_points, pickup_skill_points):
        return jsonify(
            getRandomSkillsAndRoleWithPickups(
                career_skill_points, pickup_skill_points
            )
        )
