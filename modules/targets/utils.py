from fastapi import HTTPException

VALID_TYPES = {"New", "Modification", "Renewal"}

def validate_target_data(target_name: str, target_number: str, type: str) -> bool:
    if not target_name or len(target_name) > 255:
        raise HTTPException(status_code=400, detail="Target name must be between 1 and 255 characters")
    if not target_number or len(target_number) > 100:
        raise HTTPException(status_code=400, detail="Target number must be between 1 and 100 characters")
    if type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Type must be one of {VALID_TYPES}")
    return True