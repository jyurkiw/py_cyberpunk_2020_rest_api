from .lifepath_util import originsAndPersonalStyleStart
from .lifepath_util import familyBackgroundStart
from .lifepath_util import motivationsStart
from .lifepath_util import lifeEventsStart
from .lifepath_util import getLifepath

from flask import jsonify
from flask_restful import Resource


class LifepathRandomOriginsApi(Resource):
    def get(self):
        return jsonify(getLifepath(originsAndPersonalStyleStart))


class LifepathRandomFamilyApi(Resource):
    def get(self):
        return jsonify(getLifepath(familyBackgroundStart))


class LifepathRandomMotivationsApi(Resource):
    def get(self):
        return jsonify(getLifepath(motivationsStart))


class LifepathRandomLifeEventsApi(Resource):
    def get(self):
        return jsonify(getLifepath(lifeEventsStart))


class LifepathRandomCompleteApi(Resource):
    def get(self):
        return jsonify(
            getLifepath(
                [
                    originsAndPersonalStyleStart,
                    familyBackgroundStart,
                    motivationsStart,
                    lifeEventsStart,
                ]
            )
        )


class LifepathRandomStyleAndMotivationsApi(Resource):
    def get(self):
        return jsonify([originsAndPersonalStyleStart, motivationsStart])


class LifepathRandomFamilyAndEventsApi(Resource):
    def get(self):
        return jsonify([familyBackgroundStart, lifeEventsStart])
