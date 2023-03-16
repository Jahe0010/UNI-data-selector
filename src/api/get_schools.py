from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getSchools")
async def get_school() -> list:
    db = connect()
    cursor = db.cursor()
    sql = "Select name from school"
    cursor.execute(sql)
    rows = cursor.fetchall()

    response = []
    for school in rows:

        response.append({"name": school[0]})

    db.close()
    return response
