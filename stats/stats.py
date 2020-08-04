from .stats_util import getDefaultStatBlock
from .stats_util import finalizeStatBlock

from flask import jsonify
from flask import request
from flask_restful import Resource


class StatBlockApi(Resource):
    def get(self, points):
        return jsonify(getDefaultStatBlock(points))


class StatBlockFinalizeApi(Resource):
    def post(self):
        return jsonify(finalizeStatBlock(request.json))
