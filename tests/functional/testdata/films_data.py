import uuid
from tests.functional.testdata.base_data import id_good_1, id_good_2

es_films_data_1 = {
    "imdb_rating": 8.5,
    "title": "The Star",
    "description": "New World",
    "genre": [
        {"uuid": str(uuid.uuid4()), "name": "Action"},
        {"uuid": str(uuid.uuid4()), "name": "Sci-Fi"},
    ],
    "directors": [
        {"uuid": str(uuid.uuid4()), "full_name": "Stan"},
        {"uuid": str(uuid.uuid4()), "full_name": "Edward"},
    ],
    "actors": [
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Ann",
        },
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Bob",
        },
    ],
    "writers": [
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Ben",
        },
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Howard",
        },
    ],
}

es_films_data_2 = {
    "imdb_rating": 8.5,
    "title": "Armageddon",
    "description": "New World",
    "genre": [
        {"uuid": str(uuid.uuid4()), "name": "Action"},
        {"uuid": str(uuid.uuid4()), "name": "Sci-Fi"},
    ],
    "directors": [
        {"uuid": str(uuid.uuid4()), "full_name": "Stan"},
        {"uuid": str(uuid.uuid4()), "full_name": "Edward"},
    ],
    "actors": [
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Ann",
        },
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Bob",
        },
    ],
    "writers": [
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Ben",
        },
        {
            "uuid": str(uuid.uuid4()),
            "full_name": "Howard",
        },
    ],
}

genres_data = [
    {"uuid": id_good_1, "name": "Drama"},
    {"uuid": id_good_2, "name": "Comedy"},
]
