from random import sample
from util import db
from util import getFilteredQuery

from util import distributePoints, getDefaultValueList

from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from urllib.parse import unquote

collection = db.career_skills


class CareersListApi(Resource):
    def get(self):
        return jsonify(collection.distinct("role_name"))


class CareerSkillsForRoleApi(Resource):
    def get(self, role_name):
        return jsonify(
            getFilteredQuery(
                collection, {"role_name": role_name}, {"role_name": 0}
            )
        )


class CareerRandomSkillsByRoleApi(Resource):
    def get(self, role_name, points):
        skills = getFilteredQuery(
            collection, {"role_name": role_name}, {"role_name": 0}
        )

        # Handle "choose any N from M" skill scenarios
        skills = [
            skill for skill in skills if isinstance(skill["skill"], str)
        ] + [
            {"skill": skill, "stat": skillSelectGroup["stat"]}
            for skillSelectGroup in skills
            if isinstance(skillSelectGroup["skill"], list)
            for skill in sample(
                skillSelectGroup["skill"], skillSelectGroup["select"]
            )
        ]

        skillValues = getDefaultValueList(skills, 1)
        distributePoints(skillValues, total=points)

        for i in range(0, len(skills)):
            skills[i]["score"] = skillValues[i]

        return jsonify(skills)
