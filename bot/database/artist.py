from .models import BaseArtist, DBArtist
from .connection import mongo, COLLECTIONS
from bot.logger import LOGGER

class ArtistManager:

    @staticmethod
    async def check_exists(artist_id: str, artist_name: str):
        """Searches the Database if Artist entry already exists"""
        document = None
        try:
            assert(artist_id)
            document = await mongo.db[COLLECTIONS["artists"]].find_one(
                {"artist_id": artist_id}
            )
        except:
            LOGGER.debug("Error occured while searching using artist_id - Searching using 'name' instead")
            document = await mongo.db[COLLECTIONS["artists"]].find_one(
                {"name": artist_name}
            )
        return document is not None


    @staticmethod
    async def insert_artist(data: BaseArtist):
        artist = DBArtist(**data.dict())
        await mongo.db[COLLECTIONS["artists"]].insert_one(artist.dict(by_alias=True, exclude_unset=True))


