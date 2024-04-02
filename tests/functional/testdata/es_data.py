import uuid

id_good = str(uuid.uuid4())
id_bad = str(uuid.uuid4())
id_invalid = "definitely not ID"

ids = [str(uuid.uuid4()) for _ in range(10)]


es_films_data = {
        # "uuid": str(uuid.uuid4()),
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
                "uuid": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95",
                "full_name": "Ann",
            },
            {
                "uuid": "fb111f22-121e-44a7-b78f-b19191810fbf",
                "full_name": "Bob",
            },
        ],
        "writers": [
            {
                "uuid": "caf76c67-c0fe-477e-8766-3ab3ff2574b5",
                "full_name": "Ben",
            },
            {
                "uuid": "b45bd7bc-2e16-46d5-b125-983d356768c6",
                "full_name": "Howard",
            },
        ],
    }

es_genres_data = [
    {
        "uuid": str(uuid.uuid4()),
        "name": "Action",
        "description": "piu-piu, bah-bah",
    }
    for _ in range(60)
]

es_persons_data = [
    {
        "uuid": str(uuid.uuid4()),
        "full_name": "Antinio Banderos",
        "films": [
            {
                "uuid": "caf76c67-c0fe-477e-8766-3ab3ff2574b5",
                "title": "Zorro",
                "imdb_rating": 10,
                "roles": ["actor", "director"],
            },
            {
                "uuid": "8c3a9002-d379-4d75-ad4e-429ea5b29df8",
                "title": "Spy kids",
                "imdb_rating": 1,
                "roles": ["actor", "writer"],
            },
        ],
    }
    for _ in range(60)
]
