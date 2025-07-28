import re
from typing import Dict


def paginate(limit: int = 10, page: int = 1) -> Dict[str, int]:
    skip = (page - 1) * limit
    return {"limit": limit, "skip": skip}


def parse_range_header(range_header: str, file_size: int):
    if not range_header or not range_header.startswith("bytes="):
        return 0, file_size - 1

    match = re.match(r"bytes=(\d+)-(\d*)", range_header)
    if not match:
        return 0, file_size - 1

    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else file_size - 1

    end = min(end, file_size - 1)
    return start, end