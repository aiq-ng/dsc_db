def validate_profile_data(full_name: str, bio: str) -> bool:
    if not full_name or len(full_name) > 255:
        return False
    if bio and len(bio) > 1000:
        return False
    return True