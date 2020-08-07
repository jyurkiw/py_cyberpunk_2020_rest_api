from util import db
from util import getFilteredQuery

from random import choices

_armorCollection = db.armor
_weaponsCollection = db.weapons

_locations = ["head", "torso", "legs"]


def getProtectedLocations(armorList):
    locations = {l: False for l in _locations}
    for armor in armorList:
        for location in _locations:
            locations[location] = locations[location] or armor[location]
    return locations


def getArmorFilter(armorList):
    protectedLocations = getProtectedLocations(armorList)
    return {
        "$and": [
            {location: False}
            for location in protectedLocations
            if protectedLocations[location]
        ]
    }


def getWeightedEquipmentNum(weights):
    """Returns a weighted random number between 1 and 3 based on passed weights.
    TODO: Too much hardcode value. There is a lot of room for improvement here.
    """
    return choices([1, 2, 3], weights=weights, k=1)[0]


def getRandomWeapons(numWeapons):
    """Returns a random list of weapons of numWeapons size.
    """
    return getFilteredQuery(_weaponsCollection, {"random_count": numWeapons},)


def getRandomArmors(numArmors):
    """Returns a random list of armor of numArmors size.
    Armors will not overlap protected locations.
    """
    armor = []
    filter_base = {"random_count": 1}

    for aIdx in range(0, numArmors):
        filter = getArmorFilter(armor)
        filter.update(filter_base)
        result = getFilteredQuery(_armorCollection, filter)
        armor += result
    return armor
