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
        target.target_name, target.target_number, target.file_number, target.folder, target.offence_id,
        target.operator_id, target.type, target.origin, target.target_date, target.metadata
    )

@router.get("/{target_id}")
async def get_target(target_id: int, current_user=Depends(get_current_user)):
    return await target_manager.get_target(target_id)

@router.get("/")
async def get_all_targets(
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user)
):
    # Get paginated targets and total count from manager
    targets, total = await target_manager.get_all_targets(skip, limit)
    
    # Calculate next and previous page URLs
    base_url = "/targets/"
    next_page = f"{base_url}?skip={skip + limit}&limit={limit}" if skip + limit < total else None
    previous_page = f"{base_url}?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None
    print("paginated")
    return {
        "targets": targets,
        "total": total,
        "next_page": next_page,
        "previous_page": previous_page
    }


@router.get("/search/")  # Custom response with pagination metadata
async def search_targets(
    target_name: str = None,
    target_number: str = None,
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user)
):
    if not target_name and not target_number:
        raise HTTPException(status_code=400, detail="At least one search parameter (target_name or number) is required")
    return await target_manager.search_targets(target_name, target_number, skip, limit)

@router.put("/{target_id}")
async def update_target(target_id: int, target: TargetUpdate, current_user=Depends(get_current_user)):
    return await target_manager.update_target(target_id, target.dict())

@router.delete("/{target_id}")
async def delete_target(target_id: int, current_user=Depends(get_current_user)):
    return await target_manager.delete_target(target_id)


@router.patch("/{target_id}/flag")
async def flag_target(target_id: int, flagged: bool = True, current_user=Depends(get_current_user)):
    return await target_manager.flag_target(target_id, flagged)


