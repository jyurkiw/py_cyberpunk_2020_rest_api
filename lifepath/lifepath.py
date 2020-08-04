from util import db
from util import getFilteredQuery

from random import choice

from flask import jsonify
from flask_restful import Resource

# from flask_restful import reqparse
# from urllib.parse import unquote

collection = db.lifepath


def getLifepath(step, tableName):
    lifepath = []
    repeat = None
    while tableName and not repeat:
        result = getFilteredQuery(
            collection,
            {"step": step, "table_name": tableName, "random_count": 1},
            {"step": 0},
        )
        if result:
            result = result[0]
            repeat = result.get("repeat", False)
            tableName = result.get("redirect", False)
            choose = result.get("choose", True)
            if tableName:
                tableName = tableName if not choose else choice(tableName)
                del result["redirect"]
            if repeat and tableName:
                del result["repeat"]
                result["data"] = [
                    getLifepath(step, tableName) for sibling in range(0, repeat)
                ]
            elif not choose and tableName:
                del result["choose"]
                result["data"] = [getLifepath(step, tn) for tn in tableName]
            lifepath.append(result)
        else:
            break

    return lifepath


class LifepathRandomOriginsApi(Resource):
    def get(self):
        return jsonify(getLifepath("Origins and Personal Style", "Clothes"))


class LifepathRandomFamilyApi(Resource):
    def get(self):
        return jsonify(getLifepath("Family Background", "Family Ranking"))


class LifepathRandomMotivationsApi(Resource):
    def get(self):
        return jsonify(getLifepath("Motivations", "Personality Traits"))


class LifepathRandomLifeEventsApi(Resource):
    def get(self):
        return jsonify(getLifepath("Life Events", "Age"))
