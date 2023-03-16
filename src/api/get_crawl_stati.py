from fastapi import APIRouter
from db.connector import connect

router = APIRouter(prefix="/selector")


@router.get("/getCrawlStageDirector")
def get_crawl_status_director():
    db = connect()
    cursor = db.cursor()
    sql = "Select id, name, crawl_stage from director where crawl_stage != 'finished'"

    result = {
        "auto": [],
        "manual": []
    }

    try:
        cursor.execute(sql)
        directors = cursor.fetchall()
    except Exception as e:
        print(e)
        return result

    for director in directors:
        director_obj = {
            "id": director[0],
            "name": director[1],
            "crawl_stage": director[2]
        }

        if director[2] == "manual_to_refactor":
            result["manual"].append(director_obj)
        else:
            result["auto"].append(director_obj)

    db.close()
    return result


@router.get("/getCrawlStageMovie")
def get_crawl_status_movie():
    db = connect()
    cursor = db.cursor()
    sql = "Select id, titel, crawl_stage from movies where crawl_stage != 'finished'"

    result = {
        "auto": [],
        "manual": []
    }

    try:
        cursor.execute(sql)
        movies = cursor.fetchall()
    except Exception as e:
        print(e)
        return result

    for movie in movies:
        movie_obj = {
            "id": movie[0],
            "titel": movie[1],
            "crawl_stage": movie[2]
        }

        if movie[2] == "manual_to_refactor":
            result["manual"].append(movie_obj)
        else:
            result["auto"].append(movie_obj)
    db.close()
    return result


@router.get("/getCrawlStageLocation")
def get_crawl_status_movie():
    db = connect()
    cursor = db.cursor()
    sql = "Select id, name, region, country, crawl_stage from location where crawl_stage != 'finished'"

    result = {
        "auto": [],
        "manual": []
    }

    try:
        cursor.execute(sql)
        locations = cursor.fetchall()
    except Exception as e:
        print(e)
        return result

    for location in locations:
        location_obj = {
            "id": location[0],
            "name": location[1],
            "region": location[2],
            "country": location[3],
            "crawl_stage": location[4]
        }

        if location[4] == "manual_to_refactor":
            result["manual"].append(location_obj)
        else:
            result["auto"].append(location_obj)
    db.close()
    return result


@router.get("/getCrawlStageSchool")
def get_crawl_status_movie():
    db = connect()
    cursor = db.cursor()
    sql = "Select name, crawl_stage from school where crawl_stage != 'finished'"

    result = {
        "auto": [],
        "manual": []
    }

    try:
        cursor.execute(sql)
        schools = cursor.fetchall()
    except Exception as e:
        print(e)
        return result

    for school in schools:
        school_obj = {
            "name": school[0],
            "crawl_stage": school[1]
        }

        if school[1] == "manual_to_refactor":
            result["manual"].append(school_obj)
        else:
            result["auto"].append(school_obj)
    db.close()
    return result
