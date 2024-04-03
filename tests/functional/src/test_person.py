import pytest

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
        ({"person_id": id_good_1}, {"status": 200, "length": 2, "uuid": id_good_1, "films": person_re_1}),
        ({"person_id": id_good_2}, {"status": 200, "length": 2, "uuid": id_good_2, "films": person_re_2}),
        ({"person_id": id_bad}, {"status": 404}),
        ({"person_id": id_invalid}, {"status": 422}),
        ({"person_id": id_invalid_blank}, {"status": 404}),
    ],
)
@pytest.mark.asyncio
async def test_person_films(
    make_get_request, es_write_data, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids[:10]]
    template[0] = {"uuid": id_good_1}
    template[-1] = {"uuid": id_good_2}
    for id_1, id_2 in zip(template[:5], template[5:]):
        id_1.update(es_persons_data_1)
        id_2.update(es_persons_data_2)
    await es_write_data(template, module="persons")

    response = await make_get_request(f"/persons/{query_data.get('person_id')}/film", query_data)
    body, status = response

    assert status == expected_answer.get("status")
    if status == 200:
        assert len(body) == expected_answer.get("length")
        assert body == expected_answer.get("films")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"person_id": id_good_1}, {"status": 200, "uuid": id_good_1}),
        ({"person_id": id_bad}, {"status": 404, "uuid": id_bad}),
        ({"person_id": id_invalid}, {"status": 422}),
        ({"person_id": id_invalid_blank}, {"status": 404}),
    ],
)
@pytest.mark.asyncio
async def test_one_person(make_get_request, es_write_data, query_data, expected_answer):
    template = [{"uuid": id_good_1}]
    template[0].update(es_persons_data_1)
    await es_write_data(template, module="persons")

    response = await make_get_request(f"/persons/{query_data.get('person_id')}")
    body, status = response

    assert status == expected_answer.get("status")
    if status == 200:
        assert body.get("uuid") == expected_answer.get("uuid")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "Antinio"}, {"status": 200, "length": 5}),
        ({"query": "antonio banderas"}, {"status": 200, "length": 5}),
        ({"query": "onio anDera"}, {"status": 200, "length": 5}),
        ({"query": "pit"}, {"status": 200, "length": 5}),
        ({"query": "onio"}, {"status": 404}),
        ({"query": "Mashed potato"}, {"status": 404}),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request, es_write_data, query_data, expected_answer
):
    template = [{"uuid": id} for id in ids[:10]]
    for id_1, id_2 in zip(template[:5], template[5:]):
        id_1.update(es_persons_data_1)
        id_2.update(es_persons_data_2)
    await es_write_data(template, module="persons")

    response = await make_get_request("/persons/search/", query_data)
    body, status = response

    assert status == expected_answer.get("status")
    if status == 200:
        assert len(body) == expected_answer.get("length")
        for doc in body:
            assert doc.get("uuid") in ids
