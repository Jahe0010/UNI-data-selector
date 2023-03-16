from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getNames")
async def get_names() -> list:
    db = connect()
    cursor = db.cursor()
    sql = "Select name from director"
    cursor.execute(sql)
    rows = cursor.fetchall()

    response = []
    for name in rows:
        response.append(name[0])

    sql = "Select titel from movies"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for name in rows:
        response.append(name[0])

    sql = "Select name from nicknames"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for name in rows:
        response.append(name[0])
    db.close()
    return response
