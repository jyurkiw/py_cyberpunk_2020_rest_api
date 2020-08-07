from pymongo import MongoClient
from pyconst import loadConstantsFile
from random import choices
import os

if os.path.exists(".dbConstants"):
    _db_consts = loadConstantsFile("DatabaseConstants", ".dbConstants")
    db = MongoClient()[_db_consts.dbName]


def getFilteredQuery(collection, filter, projection={}):
    """Returns the results of the passed query.
    Allows the {"random_count": int} filter which is just a sentinel value
    for {$sample: {size: int}} in the aggregate pipeline.

    [projection] will never allow for the inclusion of _id.
    """
    projection.update({"_id": 0})
    filter = {k: filter[k] for k in filter if filter[k]}
    randomCount = filter.get("random_count", None)
    if randomCount:
        filter = {k: filter[k] for k in filter if k != "random_count"}
        return list(
            collection.aggregate(
                [
                    {"$match": filter},
                    {"$sample": {"size": randomCount}},
                    {"$project": projection},
                ]
            )
        )
    else:
        return [d for d in collection.find(filter, projection)]


def getDefaultValueList(valueIndexMap, defaultValue):
    return [defaultValue for i in range(0, len(valueIndexMap))]


def mergeIndiciesToValuesByMap(valueList, valueIndexMap):
    """Package a list of stats for REST delivery according to the corrisponding
    valueIndexMap.
    """
    if len(valueList) != len(valueIndexMap):
        raise Exception("Stats: Value list and value index map did not match.")
    return {valueIndexMap[i]: valueList[i] for i in range(len(valueList))}


def incrementAtIndex(valueList, index, max):
    """Returns True if the value incremented."""
    originalValue = valueList[index]
    valueList[index] += 1 if valueList[index] < max else 0
    return valueList[index] != originalValue


def convertDictToValueNameList(valueDict):
    """Returns a list of name/value dictionaries. Not recursive. Scrubs empties."""
    return [
        {"name": k, "value": valueDict[k]} for k in valueDict if valueDict[k]
    ]


def convertValueNameListToDict(valueList):
    """Returns a dictionary formed from a list of name/value pairs. Not recursive."""
    return {k["name"]: k["value"] for k in valueList}


def distributePoints(valueList, **args):
    """Returns a list of random numbers that line up with a valueIndexMap.
    """
    points = args.get("points", args.get("total", 80) - sum(valueList))
    max = args.get("max", 10)
    weights = args.get("weights", [])
    if sum(valueList) + points > len(valueList) * max:
        return [max for i in valueList]

    # Set the weights, defaulting to all 1
    weights = weights if weights else [1 for i in range(0, len(valueList))]

    # We're distributing based on an index list because weighting requires using
    # random.choices
    indexList = [i for i in range(0, len(valueList))]

    while points > 0:
        points -= (
            1
            if incrementAtIndex(
                valueList, choices(indexList, weights, k=1)[0], max
            )
            else 0
        )

    return valueList
