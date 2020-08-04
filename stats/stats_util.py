from util import (
    distributePoints,
    mergeIndiciesToValuesByMap,
    getDefaultValueList,
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
    "humanity": lambda sb: sb["empathy"] * 10,
    "reputation": lambda sb: 0,
}

_recalculatedIndexMap = {
    "current_reflex": lambda sb: sb["reflex"] - sb["encumbrance_value"],
    "current_empathy": lambda sb: floor(sb["humanity"] / 10),
}


def calculateStats(valueDict, calculatedIndexMap=_defaultCalculatedIndexMap):
    """Calculate calculated stats."""
    for key in calculatedIndexMap:
        valueDict[key] = calculatedIndexMap[key](valueDict)
    return valueDict


def getDefaultStatBlock(totalStatPoints):
    baseStats = getDefaultValueList(_valueIndexMap, 1)
    distributePoints(baseStats, total=totalStatPoints)
    statBlock = mergeIndiciesToValuesByMap(baseStats, _valueIndexMap)
    calculatedStats = calculateStats(statBlock)
    statBlock.update(calculatedStats)

    return statBlock


def finalizeStatBlock(statBlock):
    return calculateStats(statBlock, _recalculatedIndexMap)
