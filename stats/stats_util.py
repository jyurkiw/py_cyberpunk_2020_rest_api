from util import (
    distributePoints,
    mergeIndiciesToValuesByMap,
    getDefaultValueList,
    convertDictToValueNameList,
    convertValueNameListToDict,
)

from math import floor

# The default list of stats
_valueIndexMap = [
    "intelligence",
    "reflex",
    "technical",
    "cool",
    "attractiveness",
    "luck",
    "movement_allowance",
    "body",
    "empathy",
]

# Calculated stat calculators
_defaultCalculatedIndexMap = {
    "run": lambda sb: sb["movement_allowance"] * 3,
    "leap": lambda sb: sb["run"] / 4,
    "lift": lambda sb: sb["body"] * 40,
    "encumbrance_value": lambda sb: 0,
    "reputation": lambda sb: 0,
}

_recalculatedIndexMap = {
    "current_reflex": lambda sb: sb["reflex"] - sb["encumbrance_value"],
    "humanity": lambda sb: (sb["empathy"] * 10) - sb["humanity_loss"],
    "current_empathy": lambda sb: floor(sb["humanity"] / 10),
}


def calculateStats(valueDict, calculatedIndexMap=_defaultCalculatedIndexMap):
    """Calculate calculated stats."""
    for key in calculatedIndexMap:
        valueDict[key] = calculatedIndexMap[key](valueDict)
    return valueDict


def getDefaultStatBlock(totalStatPoints):
    """Returns a randomized statBlock with [totalStatPoints] character points.

    Params:
        totalStatPoints int The number of character points in the stat block.
    """
    baseStats = getDefaultValueList(_valueIndexMap, 1)
    distributePoints(baseStats, total=totalStatPoints)
    statBlock = mergeIndiciesToValuesByMap(baseStats, _valueIndexMap)
    statBlock.update(calculateStats(statBlock))

    return convertDictToValueNameList(statBlock)


def finalizeStatBlock(statList):
    """Returns a statBlock with post-creation calculated stats added.
    Post-creation stats are things like current reflex, current empathy,
    and humanity after humanity_loss for cybernetics.

    Params:
        statList list A list of stat nameValue dicts.
    """
    statBlock = convertValueNameListToDict(statList)
    statBlock.update(calculateStats(statBlock, _recalculatedIndexMap))
    return convertDictToValueNameList(statBlock)
