from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getCountries")
async def get_country() -> list:
    db = connect()
    cursor = db.cursor()
    sql = "Select name from country"
    cursor.execute(sql)
    rows = cursor.fetchall()

    response = []
    for country in rows:

        response.append({"name": country[0]})

    db.close()
    return response
