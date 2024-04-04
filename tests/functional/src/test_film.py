import pytest

from tests.functional.testdata.films_data import (
    es_films_data_1,
    es_films_data_2,
    genres_data,
)

from tests.functional.testdata.base_data import (
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
        ({"film_id": id_bad}, {"status": 404}),
        ({"film_id": id_invalid}, {"status": 422}),
    ],
)
@pytest.mark.asyncio
async def test_one_film(
    make_get_request, es_write_data, es_delete_data, clear_cache, query_data, expected_answer
):
    template = [{"uuid": id_good_1}]
    template[0].update(es_films_data_1)
    await es_write_data(template, module="films")

    await clear_cache()
    path = f"/films/{query_data.get('film_id')}"
    es_response = await make_get_request(path)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == 200:
        await es_delete_data(module="films")
        rd_response = await make_get_request(path)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert es_body.get("uuid") == expected_answer.get("uuid")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"sort": "imdb_rating"},
            {
                "status": 200,
                "field": "imdb_rating",
                "check_param": 1,
            },
        ),
        (
            {"sort": "-imdb_rating"},
            {
                "status": 200,
                "field": "imdb_rating",
                "check_param": 10,
            },
        ),
        (
            {"sort": "title.raw"},
            {
                "status": 200,
                "field": "title",
                "check_param": "a",
            },
        ),
        (
            {"sort": "-title.raw"},
            {
                "status": 200,
                "field": "title",
                "check_param": "s",
            },
        ),
        ({"sort": "not valid field"}, {"status": 422}),
        ({}, {"status": 200}),
    ],
)
@pytest.mark.asyncio
async def test_sorted(
    make_get_request, es_write_data, es_delete_data, clear_cache, query_data, expected_answer
):

    template = [{"uuid": id} for id in ids[:10]]
    for id in template:
        id.update(es_films_data_1)
    # letters_to_sort_by = "acegikmoqs"
    letters_to_sort_by = string.ascii_letters[:20:2]
    for index in range(10):
        template[index]["imdb_rating"] = float(index + 1)
        template[index]["title"] = letters_to_sort_by[index]
    await es_write_data(template, module="films")

    await clear_cache()
    path = "/films/"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == 200:
        await es_delete_data(module="genres")
        rd_response = await make_get_request(path, query_data)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert len(es_body) == len(template)
        for doc in es_body:
            assert doc.get("uuid") in ids
        assert es_body[0].get(expected_answer.get("field")) == expected_answer.get(
            "check_param"
        )


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"genre": id_good_1},
            {"status": 200, "length": 3, "genre": genres_data},
        ),
        ({"genre": id_bad}, {"status": 404}),
        ({"genre": id_invalid}, {"status": 422}),
    ],
)
@pytest.mark.asyncio
async def test_filtered(
    make_get_request, es_write_data, es_delete_data, clear_cache, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids[:10]]
    for id in template:
        id.update(es_films_data_1)
    if expected_answer.get("status") == 200:
        for doc in template[: expected_answer.get("length")]:
            doc["genre"] = genres_data
    await es_write_data(template, module="films")

    await clear_cache()
    path = "/films/"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == 200:
        await es_delete_data(module="genres")
        rd_response = await make_get_request(path, query_data)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert len(es_body) == expected_answer.get("length")
        valid_ids = ids[: expected_answer.get("length")]
        for doc in es_body:
            assert doc.get("uuid") in valid_ids


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"page_number": 2, "page_size": 4},
            {"status": 200, "length": 4},
        ),
        (
            {"page_number": 3, "page_size": 4},
            {"status": 200, "length": 2},
        ),
        (
            {"page_number": 4, "page_size": 2},
            {"status": 200, "length": 2},
        ),
        (
            {"page_number": 0, "page_size": 2},
            {"status": 422},
        ),
        (
            {"page_number": 2, "page_size": 0},
            {"status": 422},
        ),
        (
            {"page_number": -1, "page_size": 2},
            {"status": 422},
        ),
        (
            {"page_number": 1, "page_size": -1},
            {"status": 422},
        ),
        (
            {"page_number": 101, "page_size": 2},
            {"status": 422},
        ),
        (
            {"page_number": 2, "page_size": 101},
            {"status": 422},
        ),
        (
            {"page_number": "not int value", "page_size": 2},
            {"status": 422},
        ),
        (
            {"page_number": 5, "page_size": "not int value"},
            {"status": 422},
        ),
    ],
)
@pytest.mark.asyncio
async def test_paginated(
    make_get_request, es_write_data, es_delete_data, clear_cache, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids[:10]]
    for id in template:
        id.update(es_films_data_1)
    await es_write_data(template, module="films")

    await clear_cache()
    path = "/films/"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == 200:
        await es_delete_data(module="genres")
        rd_response = await make_get_request(path, query_data)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert len(es_body) == expected_answer.get("length")
        for index in range(expected_answer.get("length")):
            start = (query_data.get("page_number") - 1) * query_data.get(
                "page_size"
            )
            stop = query_data.get("page_number") * query_data.get("page_size")

            assert template[start:stop][index].get("uuid") == es_body[index].get(
                "uuid"
            )


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "The Star"}, {"status": 200, "length": 5}),
        ({"query": "star"}, {"status": 200, "length": 5}),
        ({"query": "magedDon"}, {"status": 200, "length": 5}),
        ({"query": "Mashed potato"}, {"status": 404}),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request, es_write_data, es_delete_data, clear_cache, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids[:10]]
    for id_1, id_2 in zip(template[:5], template[5:]):
        id_1.update(es_films_data_1)
        id_2.update(es_films_data_2)
    await es_write_data(template, module="films")

    await clear_cache()
    path = "/films/search/"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == 200:
        await es_delete_data(module="genres")
        rd_response = await make_get_request(path, query_data)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert len(es_body) == expected_answer.get("length")
        for doc in es_body:
            assert doc.get("uuid") in ids
