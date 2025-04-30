from typing import List

from fastapi import APIRouter, Body, Depends, Request, status

from modules.auth.router import get_current_user
from modules.shared.response_handler import format_response

from .manager import BaseManager

resource = APIRouter()


@resource.post("/{resource}/", status_code=status.HTTP_201_CREATED)
async def create_a_resource(
    resource: str, resource_data: dict, current_user=Depends(get_current_user)
):
    resource_service = BaseManager()

    if resource not in await resource_service.get_all_resources():
        return format_response(
            {"message": f"Resource {resource} not found"}, status_code=404
        )

    resource_id = await resource_service.create_data(resource, resource_data)
    return format_response(resource_id)


@resource.get("/{resource}/")
async def get_all_resource(
    resource: str, request: Request, current_user=Depends(get_current_user)
):
    resource_service = BaseManager()

    filters = {}

    query_params = dict(request.query_params)
    for key, value in query_params.items():
        if key not in filters:
            filters[key] = value

    if resource not in await resource_service.get_all_resources():
        return format_response(
            {"message": f"Resource {resource} not found"}, status_code=404
        )

    resources = await resource_service.get_data(resource, filters=filters)
    return format_response(resources)


@resource.get("/{resource}/{resource_id}/")
async def get_a_resource(
    resource: str, resource_id: str, current_user=Depends(get_current_user)
):
    resource_service = BaseManager()

    if resource not in await resource_service.get_all_resources():
        return format_response(
            {"message": f"Resource {resource} not found"}, status_code=404
        )
    resource = await resource_service.get_data(
        resource, filters={"id": resource_id}
    )
    return format_response(resource)


@resource.put("/{resource}/{resource_id}/")
async def update_resource(
    resource: str,
    resource_id: str,
    resource_data: dict,
    current_user=Depends(get_current_user),
):
    resource_service = BaseManager()

    if resource not in await resource_service.get_all_resources():
        return format_response(
            {"message": f"Resource {resource} not found"}, status_code=404
        )
    resource = await resource_service.update_data(
        resource, resource_id, resource_data
    )
    return format_response(resource)


@resource.delete("/{resource}/")
async def delete_resource(
    resource: str,
    current_user=Depends(get_current_user),
    ids: List[str] = Body(...),
):

    resource_service = BaseManager()

    if resource not in await resource_service.get_all_resources():
        return format_response(
            {"message": f"Resource {resource} not found"}, status_code=404
        )
    response = await resource_service.delete_data(resource, ids)
    return format_response(response)
