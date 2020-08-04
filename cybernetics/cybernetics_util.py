from random import randint


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
