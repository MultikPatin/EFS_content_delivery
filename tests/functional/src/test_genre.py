import pytest

from tests.functional.testdata.base_data import (
    id_good_1,
    id_bad,
    id_invalid,
    ids,
)

from tests.functional.testdata.genres_data import es_genres_data


@pytest.mark.parametrize(
    "film, expected_answer",
    [
        ({"genre_id": id_good_1}, {"status": 200, "uuid": id_good_1}),
        ({"genre_id": id_bad}, {"status": 404, "uuid": id_bad}),
        ({"genre_id": id_invalid}, {"status": 422, "uuid": id_invalid}),
    ],
)
@pytest.mark.asyncio
async def test_by_id(make_get_request, es_write_data, film, expected_answer):
    template = [{"uuid": id_good_1}]
    template[0].update(es_genres_data)
    await es_write_data(template, module="genres")
    response = await make_get_request(f'/genres/{film["genre_id"]}')
    body, status = response

    assert status == expected_answer["status"]
    if body.get("uuid"):
        assert body["uuid"] == expected_answer["uuid"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"genre_id": id_good_1}, {"status": 200, "uuid": id_good_1}),
    ],
)
@pytest.mark.asyncio
async def test_one_genre(
    make_get_request,
    es_write_data,
    es_delete_data,
    clear_cache,
    query_data,
    expected_answer,
):
    template = [{"uuid": id_good_1}]
    template[0].update(es_genres_data)
    await es_write_data(template, module="genres")

    await clear_cache()
    es_response = await make_get_request(
        f"/genres/{query_data.get('genre_id')}"
    )
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == 200:
        await es_delete_data(module="genres")

        rd_response = await make_get_request(
            f"/genres/{query_data.get('genre_id')}"
        )
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert es_body.get("uuid") == expected_answer.get("uuid")
        assert rd_body.get("uuid") == expected_answer.get("uuid")


@pytest.mark.asyncio
async def test_get_genre(make_get_request, es_write_data):
    template = [{"uuid": id_good_1}]
    template[0].update(es_genres_data)
    await es_write_data(template, module="genres")
    response = await make_get_request(f"/genres/{id_good_1}")
    expected_keys = ["uuid", "name"]
    expected_body = {
        "uuid": id_good_1,
        "name": "Action",
    }
    body, status = response

    for key in body.keys():
        assert key in expected_keys, (
            "При GET-запросе к эндпоинту `api/v1/genres/{genre_id}` в ответе API должны "
            f"быть ключи `{expected_keys}`."
        )

    assert body == expected_body, (
        "При GET-запросе к эндпоинту `api/v1/genres/{genre_id}` тело ответа API "
        "отличается от ожидаемого."
    )


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
    make_get_request, es_write_data, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids[:10]]
    for id in template:
        id.update(es_genres_data)
    await es_write_data(template, module="genres")

    response = await make_get_request("/genres/", query_data)
    body, status = response

    assert status == expected_answer.get("status")
    if status == 200:
        assert len(body) == expected_answer.get("length")
        for index in range(expected_answer.get("length")):
            start = (query_data.get("page_number") - 1) * query_data.get(
                "page_size"
            )
            stop = query_data.get("page_number") * query_data.get("page_size")

            assert template[start:stop][index].get("uuid") == body[index].get(
                "uuid"
            )
