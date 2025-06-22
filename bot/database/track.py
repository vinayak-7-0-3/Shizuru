from .models import BaseTrack, DBTrack
from .connection import mongo, COLLECTIONS

class TrackManager:

    @staticmethod
    async def check_exists(track_id: str, file_id: str):
        """Searches the Database if Track already exists"""
        document = None
        try:
            assert(track_id)
            document = await mongo.db[COLLECTIONS["songs"]].find_one(
                {"track_id": track_id}
            )
        except:
            document = await mongo.db[COLLECTIONS["songs"]].find_one(
                {"file_unique_id": file_id}
            )
        return document is not None


    @staticmethod
    async def insert_track(data: BaseTrack):
        track = DBTrack(**data.dict())
        await mongo.db[COLLECTIONS["songs"]].insert_one(track.dict(by_alias=True, exclude_unset=True))



