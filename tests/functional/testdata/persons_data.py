from tests.functional.testdata.base_data import id_good_1, id_good_2

es_persons_data_1 = {
    "full_name": "Antonio Banderas",
    "films": [
        {
            "uuid": id_good_1,
            "title": "Zorro",
            "imdb_rating": 8,
            "roles": ["actor", "director"],
        },
        {
            "uuid": id_good_2,
            "title": "Spy kids",
            "imdb_rating": 1,
            "roles": ["actor", "writer"],
        },
    ],
}

es_persons_data_2 = {
    "full_name": "Brad Pitt",
    "films": [
        {
            "uuid": id_good_1,
            "title": "Meet Joe Black",
            "imdb_rating": 10,
            "roles": ["actor", "director"],
        },
        {
            "uuid": id_good_2,
            "title": "Troy",
            "imdb_rating": 8,
            "roles": ["actor", "writer"],
        },
    ],
}
person_re_1 = [
    {
        "uuid": id_good_1,
        "title": "Zorro",
        "imdb_rating": 8,
    },
    {
        "uuid": id_good_2,
        "title": "Spy kids",
        "imdb_rating": 1,
    },
]
person_re_2 = [
    {
        "uuid": id_good_1,
        "title": "Meet Joe Black",
        "imdb_rating": 10,
    },
    {
        "uuid": id_good_2,
        "title": "Troy",
        "imdb_rating": 8,
    },
]
