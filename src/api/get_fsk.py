from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getFsk")
async def get_fsk() -> list:
    db = connect()
    cursor = db.cursor()
    sql = "Select name from fsk"
    cursor.execute(sql)
    rows = cursor.fetchall()

    response = []
    for fsk in rows:

        response.append({"name": fsk[0]})

    db.close()
    return response
