from stats import getDefaultStatBlock
from stats import finalizeStatBlock

from skills import getRandomSkillsWithPickups
from skills import getRandomSkillsAndRoleWithPickups

from lifepath import getLifepath
from lifepath import originsAndPersonalStyleStart
from lifepath import familyBackgroundStart
from lifepath import motivationsStart
from lifepath import lifeEventsStart

from equipment import getRandomWeapons
from equipment import getRandomArmors
from equipment import getWeightedEquipmentNum

from cybernetics import getMaxCyberNumByRole
from cybernetics import rollRandomCybernetics

from pyconst import buildConstantsContainer

lifepathComplete = [
    originsAndPersonalStyleStart,
    familyBackgroundStart,
    motivationsStart,
    lifeEventsStart,
]
lifepathWho = [originsAndPersonalStyleStart, motivationsStart]


def getRandomSingleCharacter(**optional):
    """Returns a fully formed Randomly generated wastable or character.

    Params:
        role_name str (Optional) The role to assign. Random if omitted.
        character_points int Number of stat points.
        career_skill_points int number of career skill points.
        lifepath_restrictions str What kind of lifepath to generate [complete|who_are_you]
    """
    args = buildConstantsContainer("Args", optional)
    roleName = optional.get("role_name", None)

    statBlock = getDefaultStatBlock(args.character_points)

    pickupSkillPoints = statBlock["intelligence"] + statBlock["reflex"]
    if roleName:
        roleAndSkills = getRandomSkillsWithPickups(
            roleName, args.career_skill_points, pickupSkillPoints
        )
    else:
        roleAndSkills = getRandomSkillsAndRoleWithPickups(
            args.career_skill_points, pickupSkillPoints
        )
    roleName = roleAndSkills["role_name"]
    skills = roleAndSkills["skills"]

    if args.lifepath_restrictions == "complete":
        lifepath = getLifepath(lifepathComplete)
    elif args.lifepath_restrictions == "who_are_you":
        lifepath = getLifepath(lifepathWho)
    else:
        raise Exception(
            "Invalid lifepath_restrictions value: " + args.lifepath_restrictions
        )

    if roleName in ["Cop", "Nomad"]:
        weight = [1, 5, 2]
    elif roleName in ["Solo"]:
        weight = [1, 2, 5]
    else:
        weight = [5, 2, 1]

    weapons = getRandomWeapons(getWeightedEquipmentNum(weight))
    armor = getRandomArmors(getWeightedEquipmentNum(weight))

    cyber = rollRandomCybernetics(getMaxCyberNumByRole(roleName))

    return {
        "stat_block": statBlock,
        "role_name": roleName,
        "skills": skills,
        "lifepath": lifepath,
        "weapons": weapons,
        "armor": armor,
        "cybernetics": cyber,
    }
