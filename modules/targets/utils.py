from fastapi import HTTPException

VALID_TYPES = {"Person", "Organization", "Vehicle", "Other"}

def validate_target_data(target_name: str, number: str, type: str) -> bool:
    if not target_name or len(target_name) > 255:
        raise HTTPException(status_code=400, detail="Target name must be between 1 and 255 characters")
    if not number or len(number) > 100:
        raise HTTPException(status_code=400, detail="Target number must be between 1 and 100 characters")
    if type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Type must be one of {VALID_TYPES}")
    return True