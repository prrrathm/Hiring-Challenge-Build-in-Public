import random
import uuid


def generateWeights():
    leftWeights = [random.randint(1, 10) for _ in range(3)]
    rightWeights = [random.randint(1, 10) for _ in range(2)]
    return leftWeights, rightWeights


def generateOptions(leftWeights: list[int], rightWeights: list[int]):
    correct_answer = sum(leftWeights) - sum(rightWeights)
    options = [random.randint(1, 10) for _ in range(3)]
    return options.insert(random.randint(0, 4), correct_answer)


def verifyAnswer(
    leftWeights: list[int],
    rightWeights: list[int],
    answer: int,
):
    if sum(leftWeights) + answer - sum(rightWeights) == 0:
        return True
    elif sum(rightWeights) + answer - sum(leftWeights) == 0:
        return True
    else:
        return False


def createNewGame():
    id = uuid.uuid4()
    print("uuid", str(id))
    leftWeights, rightWeights = generateWeights()
    return {
        "gameid": id,
        "leftWeights": leftWeights,
        "rightWeights": rightWeights,
    }
