from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import AfterValidator

from src.cache.redis_repository import get_cache_repo, RedisRepository
from src.http_status_description.description import HTTPResponseDescription as HTTPDesc
from src.models.client_data import ClientData, validate_phone

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post(
    '/write_data',
    status_code=HTTPStatus.CREATED,
    responses={HTTPStatus.CONFLICT: {'description': HTTPDesc.BAD_NUMBER}}
)
async def write_client_address(
        client_data: ClientData,
        cache_repo: Annotated[RedisRepository, Depends(get_cache_repo)]
):
    if await cache_repo.get(client_data.phone):
        raise HTTPException(status_code=HTTPStatus.CONFLICT)

    await cache_repo.put(key=client_data.phone, value=client_data.address)


@router.put(
    '/write_data',
    status_code=HTTPStatus.NO_CONTENT,
    responses={HTTPStatus.BAD_REQUEST: {'description': HTTPDesc.NON_EXISTENT_NUMBER}}
)
async def update_client_address(
        client_data: ClientData,
        cache_repo: Annotated[RedisRepository, Depends(get_cache_repo)]
):
    if not await cache_repo.get(client_data.phone):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    await cache_repo.put(key=client_data.phone, value=client_data.address)


@router.get('check_data', responses={HTTPStatus.NOT_FOUND: {'description': HTTPDesc.NON_EXISTENT_NUMBER}})
async def check_client_address(
        cache_repo: Annotated[RedisRepository, Depends(get_cache_repo)],
        phone: Annotated[str, AfterValidator(validate_phone)]
):
    address = await cache_repo.get(phone)
    if not address:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return ORJSONResponse({"address": address})
