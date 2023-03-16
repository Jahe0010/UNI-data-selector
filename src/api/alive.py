from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/alive/{caller}")
@router.get("/alive")
async def alive(caller: str = "Stranger") -> Dict:
    return {"hello": caller, "alive": "I am live!"}
