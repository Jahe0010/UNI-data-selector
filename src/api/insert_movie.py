from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.connector import connect

from models.request_models import movieRequest

router = APIRouter(prefix="/selector")


@router.post("/insertMovie")
async def insert_movie(body: movieRequest):
    db = connect()
    cursor = db.cursor()

    try:
        for movie in body.movies:
            if movie.imdb_rating:
                sql = "INSERT IGNORE INTO movies (titel, released, imdb_rating, crawl_stage) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (movie.title, movie.released, movie.imdb_rating, "movie_initial"))
            else:
                sql = "INSERT IGNORE INTO movies (titel, released, crawl_stage) VALUES (%s, %s, %s)"
                cursor.execute(sql, (movie.title, movie.released, "movie_initial"))

            db.commit()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": "Database insert of movie failed. Please contact an administrator"})

    return JSONResponse(status_code=200, content={"message": "Everything started succesffuly! Crawling started!"})
