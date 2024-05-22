from http import HTTPStatus, HTTPMethod

import pytest


@pytest.mark.parametrize(
    'request_body',
    [
        {'phone': '7-845-214-58-1', 'address': 'Moscow'},
        {'phone': '8-741-254-35-7', 'address': 'Moscow'},
        {'phone': '794825747814', 'address': 'Moscow'},
        {'phone': '8917325874g', 'address': 'Moscow'},

    ]
)
@pytest.mark.asyncio
async def test_unprocessable_phone(
        request_body,
        flashdb_redis,
        make_request
):
    _, status = await make_request(HTTPMethod.POST, '/api/v1/write_data', request_body)

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_existing_phone(
        flashdb_redis,
        make_request
):
    request_body = {"phone": "89993658596", "address": "Moscow"}
    _, status = await make_request(HTTPMethod.POST, '/api/v1/write_data', request_body)
    assert status == HTTPStatus.CREATED

    _, status = await make_request(HTTPMethod.POST, '/api/v1/write_data', request_body)
    assert status == HTTPStatus.CONFLICT


@pytest.mark.parametrize(
    'request_body',
    [
        {'phone': '7-845-214-58-14', 'address': 'Moscow'},
        {'phone': '7-(965)-214-58-14', 'address': 'Moscow'},
        {'phone': '+7-125-214-58-14', 'address': 'Moscow'},
        {'phone': '8-986-214-58-14', 'address': 'Moscow'},
        {'phone': '77412145814', 'address': 'Moscow'},
        {'phone': '89632145814', 'address': 'Moscow'}
    ]
)
@pytest.mark.asyncio
async def test_get_address_by_phone(
        request_body,
        flashdb_redis,
        make_request
):
    _, _ = await make_request(HTTPMethod.POST, '/api/v1/write_data', request_body)

    phone = request_body['phone']
    _, status = await make_request(HTTPMethod.GET, '/api/v1/check_data', params={'phone': phone})

    assert status == HTTPStatus.OK


@pytest.mark.parametrize(
    'request_body',
    [
        {'phone': '7-845-214-67-25', 'address': 'Moscow'},
        {'phone': '+7-125-581-64-91', 'address': 'Moscow'},
        {'phone': '89632167514', 'address': 'Moscow'}

    ]
)
@pytest.mark.asyncio
async def test_update_address(
        request_body,
        flashdb_redis,
        make_request
):
    _, status = await make_request(HTTPMethod.PUT, '/api/v1/write_data', request_body)
    assert status == HTTPStatus.BAD_REQUEST

    _, _ = await make_request(HTTPMethod.POST, '/api/v1/write_data', request_body)

    _, status = await make_request(HTTPMethod.PUT, '/api/v1/write_data', request_body)
    assert status == HTTPStatus.NO_CONTENT
