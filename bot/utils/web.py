import re

from typing import Dict, Optional
from pyrogram.file_id import FileId
from pyrogram import Client
from .errors import FileNotFound


def paginate(limit: int = 10, page: int = 1) -> Dict[str, int]:
    skip = (page - 1) * limit
    return {"limit": limit, "skip": skip}


def is_media(message):
    return next((getattr(message, attr) for attr in ["document", "photo", "video", "audio", "voice", "video_note", "sticker", "animation"] if getattr(message, attr)), None)


async def get_file_ids(client: Client, chat_id: int, message_id: int) -> Optional[FileId]:
    message = await client.get_messages(chat_id, message_id)
    if message.empty:
        raise FileNotFound
    file_id = file_unique_id = None
    if media := is_media(message):
        file_id, file_unique_id = FileId.decode(
            media.file_id), media.file_unique_id
    setattr(file_id, 'file_name', getattr(media, 'file_name', ''))
    setattr(file_id, 'file_size', getattr(media, 'file_size', 0))
    setattr(file_id, 'mime_type', getattr(media, 'mime_type', ''))
    setattr(file_id, 'unique_id', file_unique_id)
    return file_id


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