import uvicorn
from fastapi import FastAPI
from api import alive, get_genres, get_results, get_fsk, get_schools, get_country, get_directors, get_crawl_stati, insert_movie, get_names
from starlette.requests import Request
from starlette.responses import Response

# Initialize FastAPI
selector = FastAPI()


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # you probably want some kind of logging here
        return Response("Internal server error", status_code=500)


selector.middleware('http')(catch_exceptions_middleware)

# Include the routes
selector.include_router(alive.router)
selector.include_router(get_genres.router)
selector.include_router(get_fsk.router)
selector.include_router(get_results.router)
selector.include_router(get_schools.router)
selector.include_router(get_country.router)
selector.include_router(get_directors.router)
selector.include_router(get_names.router)
selector.include_router(get_crawl_stati.router)
selector.include_router(insert_movie.router)

if __name__ == "__main__":
    uvicorn.run("main:selector", host="0.0.0.0", port=3000)
