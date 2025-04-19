from fastapi import APIRouter, HTTPException
from models.game import createNewGame, verifyAnswer
from schemas.game import GameData

router = APIRouter()


@router.get("/start-new-game")
def start_new_game():
    game = createNewGame()
    return game


@router.post("/submit-answer")
def submit_answer(data: GameData):
    game_id = data.gameid
    left = data.leftWeights
    right = data.rightWeights
    answer = data.answer

    status = verifyAnswer(rightWeights=right, leftWeights=left, answer=answer)

    return {
        "received": True,
        "gameid": game_id,
        "left": left,
        "right": right,
        "status": "Correct" if status else "Incorrect",
    }
