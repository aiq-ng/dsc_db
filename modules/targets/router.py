from fastapi import APIRouter, Depends, HTTPException
from typing import List
from modules.targets.manager import TargetManager
from modules.targets.models import TargetCreate, TargetUpdate, TargetResponse
from modules.auth.router import get_current_user

router = APIRouter()
target_manager = TargetManager()

@router.post("/")
async def create_target(target: TargetCreate, current_user=Depends(get_current_user)):
    return await target_manager.create_target(
        target.target_name, target.number, target.folder, target.offence_id,
        target.operator_id, target.type, target.origin, target.target_date, target.metadata
    )

@router.get("/{target_id}")
async def get_target(target_id: int, current_user=Depends(get_current_user)):
    return await target_manager.get_target(target_id)

@router.get("/")
async def get_all_targets(skip: int = 0, limit: int = 100, current_user=Depends(get_current_user)):
    return await target_manager.get_all_targets(skip, limit)


@router.get("/search/")
async def search_targets(
    target_name: str = None,
    number: str = None,
    current_user=Depends(get_current_user)
):
    if not target_name and not number:
        raise HTTPException(status_code=400, detail="At least one search parameter (target_name or number) is required")
    return await target_manager.search_targets(target_name, number)

@router.put("/{target_id}")
async def update_target(target_id: int, target: TargetUpdate, current_user=Depends(get_current_user)):
    return await target_manager.update_target(target_id, target.dict())

@router.delete("/{target_id}")
async def delete_target(target_id: int, current_user=Depends(get_current_user)):
    return await target_manager.delete_target(target_id)


