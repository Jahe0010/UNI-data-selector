from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getDirectorNames")
async def get_director_names() -> list:
    db = connect()
    cursor = db.cursor()
    sql = "Select name from director"
    cursor.execute(sql)
    rows = cursor.fetchall()

    response = []
    for director in rows:

        response.append(director[0])

    db.close()
    return response
