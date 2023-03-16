from fastapi import APIRouter
from db.connector import connect
from models.request_models import directorsRequest

router = APIRouter(prefix="/selector")


@router.post("/getDirectors")
async def get_directors(body: directorsRequest) -> object:
    filters = body.filters
    search_string = body.searchString
    sort = body.sort if body.sort else "id"

    directors, total_items = get_directors_request(filters, body.size, body.row, sort, search_string)
    row = body.row if body.row else 1
    size = body.size if body.size else len(directors)

    response = {
        "row": row,
        "size": size,
        "totalItems": total_items,
        "directors": directors
    }
    return response


def get_index(item, key, target):
    for index, x in enumerate(item):
        if x[key] == target:
            return index
    return -1


def get_directors_request(filters, size, row, sort, search_string=None):
    db = connect()
    cursor = db.cursor()

    try:
        sql = "Select d.id from director d join MRG as mrg on mrg.Director = d.id join movies m on m.id = mrg.Movie left join location l on d.place_of_birth = l.id left join country c on c.name = l.country  join nicknames n on n.director = d.id left join school s on s.id = d.school Where d.date_of_death is NULL and d.active_until is NULL"

        for element in filters:
            if element["name"] in ["country", "fsk", "genre", "sex", "budget", "money_earned", "imdb_rating"] or element["object"] in ["school"]:
                sql += " AND {t}.{x} {o} {y}".format(
                    t=element["object"][0] if not element["object"] == "mrg" else "mrg",
                    x=element["name"], o=element["operand"],
                    y=element["value"])
            elif element["name"] == "yearsActive":
                sql += " AND d.active_since {o} DATE_SUB(NOW(),INTERVAL {y} YEAR)".format(o=element["operand"],
                                                                                          y=element["value"])

        if search_string:
            sql += f" AND (d.name like '%{search_string}%' or m.titel like '%{search_string}%') or n.name like '%{search_string}%'"

        sql += f" Group by d.id"
    except Exception as e:
        print(e)
        return []

    if sort == "avg_earned":
        sql += " Order by avg(m.money_earned) desc"
    elif sort == "avg_budget":
        sql += " Order by avg(m.budget) desc"
    elif sort == "avg_imdb_rating":
        sql += " Order by avg(m.imdb_rating) desc"
    elif sort == "name":
        sql += " Order by d.name"
    else:
        sql += f" Order by d.id"

    print(sql)
    total_items = 0
    try:
        cursor.execute(sql)
        total_items = len(cursor.fetchall())
    except Exception as e:
        print(e)
        return []

    sql += f" Limit {size} OFFSET {row}"

    try:
        cursor.execute(sql)
        directors = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

    response = []
    for element in directors:
        try:
            sql = f"Select d.name, d.id, d.date_of_birth, s.name, d.active_since, d.sex, l.name, l.region, c.name, m.titel, m.budget, m.imdb_rating, m.money_earned, m.fsk, m.runtime, mrg.genre, l.id, n.name, m.released from MRG mrg join movies m on m.id = mrg.Movie join director d on d.id = mrg.Director join location l on d.place_of_birth = l.id join country c on c.name = l.country  join nicknames n on n.director = d.id left join school s on s.id = d.school Where d.date_of_death is NULL and d.active_until is NULL and d.id='{element[0]}'"
            cursor.execute(sql)
            directors_db = cursor.fetchall()
        except Exception as e:
            print(e)
            return []
        for director in directors_db:
            try:
                if not any("id" in obj and obj["id"] == director[1] for obj in response):
                    director_object = {
                        "name": director[0],
                        "type": "director",
                        "id": director[1],
                        "dateOfBirth": director[2],
                        "school": director[3],
                        "activeSince": director[4],
                        "sex": director[5],
                        "nicknames": [director[17]],
                        "palceOfBirth": {
                            "id": director[16],
                            "name": director[6],
                            "region": director[7],
                            "country": director[8]
                        },
                        "movies": [{
                            "title": director[9],
                            "genres": [director[15]],
                            "budget": director[10],
                            "imdb_rating": director[11],
                            "money_earned": director[12],
                            "fsk": director[13],
                            "runtime": director[14],
                            "released": director[18]
                        }]
                    }
                    response.append(director_object)
                else:
                    item = response[get_index(response, "id", director[1])]
                    if not any("title" in obj and obj["title"] == director[9] for obj in item["movies"]):
                        item["movies"].append({
                            "title": director[9],
                            "genres": [director[15]],
                            "budget": director[10],
                            "imdb_rating": director[11],
                            "money_earned": director[12],
                            "fsk": director[13],
                            "runtime": director[14],
                            "released": director[18]
                        })
                    elif not any(director[15] in obj["genres"] for obj in item["movies"]):
                        movie_item = item["movies"][get_index(item["movies"], "title", director[9])]
                        movie_item["genres"].append(director[15])
                    elif not director[17] in item["nicknames"]:
                        item["nicknames"].append(director[17])
            except Exception as e:
                print(e)

    for director in response:
        director["avg_budget"] = get_avg(director["movies"], "budget")
        director["avg_earned"] = get_avg(director["movies"], "money_earned")
        director["sum_movies"] = len(director["movies"])
        director["avg_imdb_rating"] = get_avg(director["movies"], "imdb_rating")
        director["movies"] = sorted(director["movies"], key=lambda m: m['released'], reverse=True)
    special_filtered_response = []
    try:
        for filterItem in filters:
            if filterItem["name"] in ["avg_earned", "avg_budget", "avg_imdb_rating"]:
                if filterItem["operand"] == "=":
                    response = [director for director in response if
                                director[filterItem["name"]] == filterItem["value"]]
                elif filterItem["operand"] == "<":
                    response = [director for director in response if
                                director[filterItem["name"]] <= filterItem["value"]]
                elif filterItem["operand"] == ">":
                    response = [director for director in response if
                                director[filterItem["name"]] >= filterItem["value"]]
    except Exception as e:
        print(e)
        return []

    db.close()
    if len(special_filtered_response) > 0:
        return special_filtered_response, total_items
    else:
        return response, total_items


def get_avg(movies, field):
    numbers_list = []
    try:
        for movie in movies:
            if movie[field]:
                if type(movie[field]) == str:
                    numbers_list.append(float(movie[field].replace(",", "")))
                elif type(movie[field]) == float:
                    numbers_list.append(float(movie[field]))
            else:
                numbers_list.append(0)
    except Exception as e:
        print(e)
        return 0
    return round(sum(numbers_list) / len(numbers_list), 2)
