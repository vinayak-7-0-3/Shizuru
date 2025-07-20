from typing import Dict

def paginate(limit: int = 10, page: int = 1) -> Dict[str, int]:
    skip = (page - 1) * limit
    return {"limit": limit, "skip": skip}
