from util import db
from util import getFilteredQuery

from random import randint
from random import choice

_cyberCollection = db.cybernetics


def getCyberIdList(cyberList):
    return [c["id_code"] for c in cyberList]


def rollHumanityLoss(cyber):
    loss = cyber["humanity_loss"]
    if isinstance(loss, dict):
        dice = loss["dice"]
        bonus = loss["bonus"]
        sides = 6
        if float(dice) == 0.5:
            sides = 3
            dice = 1
        if dice == -0.5:
            dice = 0
            bonus += randint(1, 3) * -1
        cyber["humanity_loss"] = (
            sum([randint(1, sides) for i in range(0, dice)]) + bonus
        )
    return cyber


def getMaxCyberNumByRole(roleName):
    """Returns the maximum number of cybernetic rolls a random hero can have.
    TODO: Figure out a better way to do this. Hard-coded values are not good.

    Params:
        roleName str The name of the role to get a value for.
    """
    return 6 if roleName == "Solo" else 3


def rollRandomCybernetics(cyNum):
    """Returns a list of random cybernetics. Cybernetic options that have
    prerequisites will automatically be given those prerequisites as a part
    of that roll (ex: Thermograph without a cybereye will be given a cybereye
    as a part of that roll.)

    Params:
        cyNum int The number of cybernetic "rolls" to make.
    """
    cyberList = getFilteredQuery(_cyberCollection, {"random_count": cyNum})

    # Roll humanity loss
    for cyber in cyberList:
        rollHumanityLoss(cyber)

    # Handle missing pre-requisite systems
    for cyber in [c for c in cyberList if c["requirements"]]:
        cyberIds = getCyberIdList(cyberList)
        requirements = cyber["requirements"]
        intersection = set(requirements) & set(cyberIds)
        if not intersection:
            req = choice(requirements)
            requiredCyber = getFilteredQuery(_cyberCollection, {"id_code": req})
            if isinstance(requiredCyber, list) and requiredCyber:
                requiredCyber = requiredCyber[0]
                rollHumanityLoss(requiredCyber)
                requiredCyber["subsystems"] = [cyber]
                cyberList.remove(cyber)
            cyberList.append(requiredCyber)
        else:
            parentId = choice(list(intersection))
            parentCyber = next(
                (c for c in cyberList if c["id_code"] == parentId), None,
            )
            rollHumanityLoss(parentCyber)
            if not parentCyber:
                raise Exception(
                    parentId
                    + " not found in "
                    + " | ".join([i["id_code"] for i in cyberList])
                )
            if not parentCyber.get("subsystems", False):
                parentCyber["subsystems"] = []
            parentCyber["subsystems"].append(cyber)
            cyberList.remove(cyber)
    return cyberList
