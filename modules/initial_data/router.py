from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from modules.auth.router import get_current_user
from modules.initial_data.manager import InitialDataManager
from modules.initial_data.models import (OffenceCreate, OffenceResponse,
                                         OffenceUpdate, OperatorCreate,
                                         OperatorResponse, OperatorUpdate)

router = APIRouter()
manager = InitialDataManager()


# Operators Endpoints
@router.post("/operators/")
async def create_operator(
    operator: OperatorCreate, current_user=Depends(get_current_user)
):
    return await manager.create_operator(operator.dict())


@router.get("/operators/{operator_id}/")
async def get_operator(
    operator_id: int, current_user=Depends(get_current_user)
):
    return await manager.get_operator(operator_id)


@router.get("/operators/")
async def get_all_operators(
    skip: int = 0, limit: int = 100, current_user=Depends(get_current_user)
):
    return await manager.get_all_operators(skip, limit)


@router.put("/operators/{operator_id}/")
async def update_operator(
    operator_id: int,
    operator: OperatorUpdate,
    current_user=Depends(get_current_user),
):
    return await manager.update_operator(operator_id, operator.dict())


@router.delete("/operators/{operator_id}/")
async def delete_operator(
    operator_id: int, current_user=Depends(get_current_user)
):
    return await manager.delete_operator(operator_id)


# Offences Endpoints
@router.post("/offences/")
async def create_offence(
    offence: OffenceCreate, current_user=Depends(get_current_user)
):
    return await manager.create_offence(offence.dict())


@router.get("/offences/{offence_id}/")
async def get_offence(offence_id: int, current_user=Depends(get_current_user)):
    return await manager.get_offence(offence_id)


@router.get("/offences/")
async def get_all_offences(
    skip: int = 0, limit: int = 100, current_user=Depends(get_current_user)
):
    return await manager.get_all_offences(skip, limit)


@router.put("/offences/{offence_id}/")
async def update_offence(
    offence_id: int,
    offence: OffenceUpdate,
    current_user=Depends(get_current_user),
):
    return await manager.update_offence(offence_id, offence.dict())


@router.delete("/offences/{offence_id}/")
async def delete_offence(
    offence_id: int, current_user=Depends(get_current_user)
):
    return await manager.delete_offence(offence_id)
