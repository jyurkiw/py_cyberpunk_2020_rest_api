from util import db
from util import distributePoints
from util import getFilteredQuery
from util import getDefaultValueList

from collections import OrderedDict
from collections import deque
from random import choice
from random import sample

_careerSkillsCollection = db.career_skills
_skillsCollection = db.skills


def getCareerSkillsForRole(roleName):
    return getFilteredQuery(
        _careerSkillsCollection, {"role_name": roleName}, {"role_name": 0},
    )


def getRandomSkillsAndRole(careerSkillPoints):
    """Return a random character role and the associated skills equal to careerSkillPoints.
    """
    roleName = choice(getRoleNames())
    return {
        "role_name": roleName,
        "skills": getRandomSkillsByRole(roleName, careerSkillPoints),
    }


def getRandomSkillsAndRoleWithPickups(careerSkillPoints, pickupSkillPoints):
    """Return a random character role, the associated skills equal to
    careerSkillPoints, and a number of additional pickup skills equal to
    pickupSkillPoints.
    """
    roleAndSkills = getRandomSkillsAndRole(careerSkillPoints)
    roleAndSkills["skills"] = addRandomPickupSkills(
        pickupSkillPoints, roleAndSkills["skills"]
    )
    return roleAndSkills


def getRandomSkillsWithPickups(roleName, careerSkillPoints, pickupSkillPoints):
    """Return the associated skills equal to careerSkillPoints for roleName, and
    a number of additional pickup skills equal to pickupSkillPoints.
    """
    skills = addRandomPickupSkills(
        pickupSkillPoints, getRandomSkillsByRole(roleName, careerSkillPoints)
    )
    return {"role_name": roleName, "skills": skills}


def getRandomSkillsByRole(roleName, careerSkillPoints):
    """Returns skills totaling careerSkillPoints for roleName.
    """
    skills = getCareerSkillsForRole(roleName)

    # Handle "choose any N from M" skill scenarios
    skills = [skill for skill in skills if isinstance(skill["skill"], str)] + [
        {"skill": skill, "stat": skillSelectGroup["stat"]}
        for skillSelectGroup in skills
        if isinstance(skillSelectGroup["skill"], list)
        for skill in sample(
            skillSelectGroup["skill"], skillSelectGroup["select"]
        )
    ]

    skillValues = getDefaultValueList(skills, 1)
    distributePoints(skillValues, total=careerSkillPoints)

    for i in range(0, len(skills)):
        skills[i]["score"] = skillValues[i]

    return skills


def getRoleNames():
    return _careerSkillsCollection.distinct("role_name")


def getSkills():
    return getFilteredQuery(_skillsCollection, {})


def buildMasterDict(skills):
    # Build masterSkills
    masterSkills = OrderedDict()
    for skill in getSkills():
        skill.update({"score": 0})
        masterSkills[skill["skill"]] = skill

    for skill in skills:
        if skill["skill"] in masterSkills:
            masterSkills[skill["skill"]]["score"] = skill["score"]
        else:
            masterSkills[skill["skill"]] = skill

    return masterSkills


def buildFinalSkillList(masterSkills, valueDeque):
    for skill in masterSkills:
        masterSkills[skill]["score"] = valueDeque.popleft()
    return [
        masterSkills[skill]
        for skill in masterSkills
        if masterSkills[skill]["score"] > 0
    ]


def addRandomPickupSkills(pickupSkillPoints, skillList):
    """Returns random pickup skills totaling pickupSkillPoints added to
    skillList.
    """
    masterSkills = buildMasterDict(skillList)

    valueList = deque(
        distributePoints(
            [masterSkills[skill]["score"] for skill in masterSkills],
            points=pickupSkillPoints,
        )
    )

    return buildFinalSkillList(masterSkills, valueList)
