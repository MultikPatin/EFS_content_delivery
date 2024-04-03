import pytest

from tests.functional.testdata.es_data import (
    es_films_data,
    id_good_1,
    id_bad,
    id_invalid,
    ids,
)

import string


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"film_id": id_good_1}, {"status": 200, "uuid": id_good_1}),
        ({"film_id": id_bad}, {"status": 404, "uuid": id_bad}),
        ({"film_id": id_invalid}, {"status": 422, "uuid": id_invalid}),
    ],
)
@pytest.mark.asyncio
async def test_by_id(make_get_request, es_write_data, query_data, expected_answer):
    template = [{"uuid": id_good_1}]
    template[0].update(es_films_data)
    await es_write_data(template, module="films")

    response = await make_get_request(f'/films/{query_data["film_id"]}')
    body, status = response
    assert status == expected_answer["status"]
    if body.get("uuid"):
        assert body["uuid"] == expected_answer["uuid"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"sort": "imdb_rating"},
            {
                "status": 200,
                "length": len(ids),
                "field": "imdb_rating",
                "check_param": 1,
            },
        ),
        (
            {"sort": "-imdb_rating"},
            {
                "status": 200,
                "length": len(ids),
                "field": "imdb_rating",
                "check_param": 10,
            },
        ),
        (
            {"sort": "title.raw"},
            {
                "status": 200,
                "length": len(ids),
                "field": "title",
                "check_param": "a" + es_films_data["title"],
            },
        ),
        (
            {"sort": "-title.raw"},
            {
                "status": 200,
                "length": len(ids),
                "field": "title",
                "check_param": "s" + es_films_data["title"],
            },
        ),
        ({"sort": "not valid field"}, {"status": 422, "length": 1}),
        ({}, {"status": 200, "length": len(ids)})
    ],
)
@pytest.mark.asyncio
async def test_sorted(
    make_get_request, es_write_data, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids][:10]
    for id in template:
        id.update(es_films_data)
    # letters_to_sort_by = "acegikmoqs"
    letters_to_sort_by = string.ascii_letters[:20:2]
    for index in range(10):
        template[index]["imdb_rating"] = float(index + 1)
        template[index]["title"] = (
            letters_to_sort_by[index] + template[index]["title"]
        )
    await es_write_data(template, module="films")

    response = await make_get_request("/films/", query_data)
    body, status = response
    assert status == expected_answer["status"]

    assert len(body) == expected_answer["length"]
    if isinstance(body, list):
        for doc in body:
            assert doc.get("uuid") in ids
        if query_data.get("sort"):
            assert (
                body[0].get(expected_answer["field"])
                == expected_answer["check_param"]
            )


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"genre": id_good_1}, {"status": 200, "length": 3, "field": "genre", "check_param": {"uuid": id_good_1, "name": "Drama"}}),
        ({"genre": id_bad}, {"status": 404, "length": 1, "field": "genre", "check_param": {"uuid": id_good_1, "name": "Drama"}}),
        ({"genre": id_invalid}, {"status": 422, "length": 1, "field": "genre", "check_param": {"uuid": id_good_1, "name": "Drama"}}),
    ],
)
@pytest.mark.asyncio
async def test_filtered(make_get_request, es_write_data, query_data, expected_answer):
    template = [{"uuid": id} for id in ids]

    for id in template:
        id.update(es_films_data)
    for doc in template[:expected_answer["length"]]:
        doc[expected_answer["field"]] = [expected_answer["check_param"]]

    await es_write_data(template, module="films")

    response = await make_get_request('/films/', query_data)
    body, status = response
    assert status == expected_answer["status"]

    assert len(body) == expected_answer["length"]
    valid_ids = ids[:expected_answer["length"]]
    if isinstance(body, list):
        for doc in body:
            assert doc.get("uuid") in valid_ids



@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"page_number": 2, "page_size": 4}, {"status": 200, "length": 4},
        ),
        (
            {"page_number": 3, "page_size": 4}, {"status": 200, "length": 2},
        ),
        (
            {"page_number": 4, "page_size": 2}, {"status": 200, "length": 2},
        ),
        (
            {"page_number": 0, "page_size": 2}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": 2, "page_size": 0}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": -1, "page_size": 2}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": 1, "page_size": -1}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": 101, "page_size": 2}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": 2, "page_size": 101}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": "not int value", "page_size": 2}, {"status": 422, "length": 1},
        ),
        (
            {"page_number": 5, "page_size": "not int value"}, {"status": 422, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_paginated(
    make_get_request, es_write_data, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids][:10]
    for id in template:
        id.update(es_films_data)
    await es_write_data(template, module="films")

    response = await make_get_request("/films/", query_data)
    body, status = response

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
    if isinstance(body, list):
        for index in range(expected_answer.get("length")):
            start = (query_data.get("page_number") - 1) * query_data.get("page_size")
            stop = query_data.get("page_number") * query_data.get("page_size")

            assert template[start:stop][index].get("uuid") == body[index].get("uuid")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "The Star"}, {"status": 200, "length": len(ids)}),
        ({"query": "star"}, {"status": 200, "length": len(ids)}),
        ({"query": "taR"}, {"status": 200, "length": len(ids)}),
        ({"query": "Mashed potato"}, {"status": 404, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request, es_write_data, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids]
    for id in template:
        id.update(es_films_data)
    await es_write_data(template, module="films")

    response = await make_get_request("/films/search/", query_data)
    body, status = response
    assert status == expected_answer["status"]

    assert len(body) == expected_answer["length"]
    if isinstance(body, list):
        for doc in body:
            assert doc.get("uuid") in ids
