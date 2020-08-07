from util import db
from util import getFilteredQuery

from random import choice

_collection = db.lifepath

# Lifepath table entry-point constants.
originsAndPersonalStyleStart = ("Origins and Personal Style", "Clothes")
familyBackgroundStart = ("Family Background", "Family Ranking")
motivationsStart = ("Motivations", "Personality Traits")
lifeEventsStart = ("Life Events", "Age")


def getLifepath(startKey, tableName=None):
    """Returns a lifepath step based on the passed step and tablename entry-point.
    Can consume both a step, tableName string pair, and a step, tableName tuple.
    """
    if isinstance(startKey, list):
        lifepath = {}
        for key, startTable in startKey:
            lifepath[key] = _getLifepath(key, startTable)
        return lifepath
    else:
        if tableName:
            return _getLifepath(*startKey)
        else:
            return _getLifepath(*startKey)


def _getLifepath(step, tableName):
    lifepath = []
    repeat = None
    while tableName and not repeat:
        result = getFilteredQuery(
            _collection,
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
                    _getLifepath(step, tableName)
                    for sibling in range(0, repeat)
                ]
            elif not choose and tableName:
                del result["choose"]
                result["data"] = [_getLifepath(step, tn) for tn in tableName]
            lifepath.append(result)
        else:
            break

    return lifepath
