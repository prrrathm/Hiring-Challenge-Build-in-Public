from pydantic import BaseModel
from typing import List, Optional


class GameData(BaseModel):
    gameid: str
    leftWeights: List[int]
    rightWeights: List[int]
    answer: int
