from typing import Optional, List

from pydantic import BaseModel


class Movies(BaseModel):
    title: str
    released: str
    imdb_rating: Optional[float]


class directorsRequest(BaseModel):
    filters: List[dict]
    searchString: Optional[str]
    row: Optional[int] = 0
    size: Optional[int] = 10
    sort: Optional[str]


class movieRequest(BaseModel):
    movies: List[Movies]
