from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getGenres")
async def get_genres() -> list:
    db = connect()
    cursor = db.cursor()
    sql = "Select name from genre"
    cursor.execute(sql)
    rows = cursor.fetchall()

    response = []
    for genre in rows:

        response.append({"name": genre[0]})

    db.close()
    return response
