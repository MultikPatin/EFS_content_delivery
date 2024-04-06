from enum import Enum


class FilmFieldsToSort(str, Enum):
    rating = "imdb_rating"
    desc_rating = "-imdb_rating"
    asc_title = "title.raw"
    desc_title = "-title.raw"
