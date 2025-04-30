from fastapi import HTTPException

VALID_THREAT_LEVELS = {"High", "Medium", "Low"}


def validate_target_data(
    target_name: str,
    file_number: str,
    type: str,
    threat_level: str | None = None,
) -> bool:
    if not target_name or len(target_name) > 255:
        raise HTTPException(
            status_code=400,
            detail="Target name must be between 1 and 255 characters",
        )
    if not file_number or len(file_number) > 100:
        raise HTTPException(
            status_code=400,
            detail="File number must be between 1 and 100 characters",
        )
    if threat_level and threat_level not in VALID_THREAT_LEVELS:
        raise HTTPException(
            status_code=400,
            detail=f"Threat level must be one of {VALID_THREAT_LEVELS}",
        )
    return True
