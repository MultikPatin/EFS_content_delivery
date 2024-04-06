import pytest
from http import HTTPStatus

from tests.functional.testdata.base_data import (
    id_good_1,
    id_bad,
    id_invalid,
    ids,
)

from tests.functional.testdata.genres_data import es_genres_data


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"genre_id": id_good_1},
            {
                "status": HTTPStatus.OK,
                "uuid": id_good_1,
                "keys": ["uuid", "name"],
            },
        ),
        ({"genre_id": id_bad}, {"status": HTTPStatus.NOT_FOUND}),
        ({"genre_id": id_invalid}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
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
    path = f"/genres/{query_data.get('genre_id')}"
    es_response = await make_get_request(path)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == HTTPStatus.OK:
        await es_delete_data(module="genres")
        rd_response = await make_get_request(path)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert es_body.get("uuid") == expected_answer.get("uuid")
        for key in es_body.keys():
            assert key in expected_answer.get("keys"), (
                "При GET-запросе к эндпоинту `api/v1/genres/{genre_id}` в ответе API должны "
                f"быть ключи `{expected_answer.get('keys')}`."
            )


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"page_number": 2, "page_size": 4},
            {"status": HTTPStatus.OK, "length": 4},
        ),
        (
            {"page_number": 3, "page_size": 4},
            {"status": HTTPStatus.OK, "length": 2},
        ),
        (
            {"page_number": 4, "page_size": 2},
            {"status": HTTPStatus.OK, "length": 2},
        ),
        (
            {"page_number": 0, "page_size": 2},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": 2, "page_size": 0},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": -1, "page_size": 2},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": 1, "page_size": -1},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": 101, "page_size": 2},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": 2, "page_size": 101},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": "not int value", "page_size": 2},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {"page_number": 5, "page_size": "not int value"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
@pytest.mark.asyncio
async def test_paginated(
    make_get_request,
    es_write_data,
    es_delete_data,
    clear_cache,
    query_data,
    expected_answer,
):
    template = [{"uuid": id} for id in ids[:10]]
    for id in template:
        id.update(es_genres_data)
    await es_write_data(template, module="genres")

    await clear_cache()
    path = "/genres/"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == HTTPStatus.OK:
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

            assert template[start:stop][index].get("uuid") == es_body[
                index
            ].get("uuid")
