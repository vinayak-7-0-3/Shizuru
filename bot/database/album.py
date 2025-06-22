from .models import BaseAlbum, DBAlbum
from .connection import mongo, COLLECTIONS

class AlbumManager:

    @staticmethod
    async def check_album_exists(album_id: str):
        """Searches the Database if Album already exists"""
        document = await mongo.db[COLLECTIONS["albums"]].find_one(
            {"album_id": album_id}
        )
        return document is not None

    @staticmethod
    async def insert_album(data: BaseAlbum):
        album = DBAlbum(**data.dict())
        await mongo.db[COLLECTIONS["albums"]].insert_one(album.dict(by_alias=True, exclude_unset=True))



