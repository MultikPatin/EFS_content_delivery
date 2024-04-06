import pytest
from http import HTTPStatus

from tests.functional.testdata.persons_data import (
    es_persons_data_1,
    es_persons_data_2,
    person_re_1,
    person_re_2,
)
from tests.functional.testdata.base_data import (
    id_good_1,
    id_good_2,
    id_bad,
    id_invalid,
    id_invalid_blank,
    ids,
)


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"person_id": id_good_1},
            {
                "status": HTTPStatus.OK,
                "length": 2,
                "uuid": id_good_1,
                "films": person_re_1,
            },
        ),
        (
            {"person_id": id_good_2},
            {
                "status": HTTPStatus.OK,
                "length": 2,
                "uuid": id_good_2,
                "films": person_re_2,
            },
        ),
        ({"person_id": id_bad}, {"status": HTTPStatus.NOT_FOUND}),
        (
            {"person_id": id_invalid},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        ({"person_id": id_invalid_blank}, {"status": HTTPStatus.NOT_FOUND}),
    ],
)
@pytest.mark.asyncio
async def test_person_films(
    make_get_request,
    es_write_data,
    es_delete_data,
    clear_cache,
    query_data,
    expected_answer,
):
    template = [{"uuid": id} for id in ids[:10]]
    template[0] = {"uuid": id_good_1}
    template[-1] = {"uuid": id_good_2}
    for id_1, id_2 in zip(template[:5], template[5:]):
        id_1.update(es_persons_data_1)
        id_2.update(es_persons_data_2)
    await es_write_data(template, module="persons")

    await clear_cache()
    path = f"/persons/{query_data.get('person_id')}/film"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == HTTPStatus.OK:
        await es_delete_data(module="persons")
        rd_response = await make_get_request(path, query_data)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert len(es_body) == expected_answer.get("length")
        assert es_body == expected_answer.get("films")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "Antonio"}, {"status": HTTPStatus.OK, "length": 5}),
        ({"query": "antonio banderas"}, {"status": HTTPStatus.OK, "length": 5}),
        ({"query": "onio anDera"}, {"status": HTTPStatus.OK, "length": 5}),
        ({"query": "pit"}, {"status": HTTPStatus.OK, "length": 5}),
        ({"query": "onio"}, {"status": HTTPStatus.NOT_FOUND}),
        ({"query": "Mashed potato"}, {"status": HTTPStatus.NOT_FOUND}),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request,
    es_write_data,
    es_delete_data,
    clear_cache,
    query_data,
    expected_answer,
):
    template = [{"uuid": id} for id in ids[:10]]
    for id_1, id_2 in zip(template[:5], template[5:]):
        id_1.update(es_persons_data_1)
        id_2.update(es_persons_data_2)
    await es_write_data(template, module="persons")

    await clear_cache()
    path = "/persons/search/"
    es_response = await make_get_request(path, query_data)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == HTTPStatus.OK:
        await es_delete_data(module="persons")
        rd_response = await make_get_request(path, query_data)
        rd_body, rd_status = rd_response
        assert es_status == rd_status
        assert es_body == rd_body
        assert len(es_body) == expected_answer.get("length")
        for doc in es_body:
            assert doc.get("uuid") in ids


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"person_id": id_good_1},
            {"status": HTTPStatus.OK, "uuid": id_good_1},
        ),
        ({"person_id": id_bad}, {"status": HTTPStatus.NOT_FOUND}),
        (
            {"person_id": id_invalid},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        ({"person_id": id_invalid_blank}, {"status": HTTPStatus.NOT_FOUND}),
    ],
)
@pytest.mark.asyncio
async def test_one_person(
    make_get_request,
    es_write_data,
    es_delete_data,
    clear_cache,
    query_data,
    expected_answer,
):
    await clear_cache()
    template = [{"uuid": id_good_1}]
    template[0].update(es_persons_data_1)
    await es_write_data(template, module="persons")

    await clear_cache()
    path = f"/persons/{query_data.get('person_id')}"
    es_response = await make_get_request(path)
    es_body, es_status = es_response

    assert es_status == expected_answer.get("status")
    if es_status == HTTPStatus.OK:
        await es_delete_data(module="persons")
        rd_response = await make_get_request(path)
        rd_body, rd_status = rd_response

        assert es_status == rd_status
        assert es_body == rd_body
        assert es_body.get("uuid") == expected_answer.get("uuid")
        assert rd_body.get("uuid") == expected_answer.get("uuid")
