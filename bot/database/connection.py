import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import Config
from ..logger import LOGGER


# easy references
COLLECTIONS = {
    'songs': 'songs',
    'artists': 'artists', 
    'albums': 'albums',
    'users': 'users',
    'playlists': 'playlists',
    'trash': 'trash',
    'liked_songs': 'liked_songs'
}

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.mongodb_url = Config.DATABASE_URL
        self.database_name = Config.DATABASE_NAME
        
    async def connect(self):
        self.client = AsyncIOMotorClient(self.mongodb_url)
        self.db = self.client[self.database_name]
        await self._create_indexes()
        LOGGER.info("MongoDB connected successfully")
        
    async def disconnect(self):
        if self.client:
            self.client.close()
            LOGGER.info("MongoDB disconnected successfully")

    async def _create_indexes(self):
        # Songs Collection Indexes
        await self.db[COLLECTIONS['songs']].create_index([("chat_id", 1), ("msg_id", 1)], unique=True)
        await self.db[COLLECTIONS['songs']].create_index([("track_id", 1), ("provider", 1)], sparse=True)
        await self.db[COLLECTIONS['songs']].create_index([("artist_id", 1), ("provider", 1)], sparse=True)
        await self.db[COLLECTIONS['songs']].create_index([("album_id", 1), ("provider", 1)], sparse=True)
        await self.db[COLLECTIONS['songs']].create_index([("artist", 1)])
        await self.db[COLLECTIONS['songs']].create_index([("file_unique_id", 1)])
        #await self.db[COLLECTIONS['songs']].create_index([("title", "text"), ("artist", "text"), ("album", "text")])
        
        # Artists Collection Indexes
        await self.db[COLLECTIONS['artists']].create_index([("artist_id", 1), ("provider", 1)], unique=True)
        #await self.db[COLLECTIONS['artists']].create_index([("name", "text")])
        await self.db[COLLECTIONS['artists']].create_index([("tags", 1)], sparse=True)
        
        # Albums Collection Indexes
        await self.db[COLLECTIONS['albums']].create_index([("album_id", 1), ("provider", 1)], unique=True)
        await self.db[COLLECTIONS['albums']].create_index([("artist_id", 1), ("provider", 1)])
        #await self.db[COLLECTIONS['albums']].create_index([("title", "text"), ("artist", "text")])
  
        # Users Collection Indexes
        await self.db[COLLECTIONS['users']].create_index([("username", 1)], unique=True)
        await self.db[COLLECTIONS['users']].create_index([("email", 1)], unique=True, sparse=True)
        await self.db[COLLECTIONS['users']].create_index([("is_admin", 1)])
        
        # LikedSongs Collection Indexes
        await self.db[COLLECTIONS['liked_songs']].create_index([("user_id", 1), ("song_id", 1)], unique=True)
        await self.db[COLLECTIONS['liked_songs']].create_index([("song_id", 1)])
        
        # Playlists Collection Indexes
        await self.db[COLLECTIONS['playlists']].create_index([("user_id", 1)])
        await self.db[COLLECTIONS['playlists']].create_index([("user_id", 1), ("name", 1)])
        #await self.db[COLLECTIONS['playlists']].create_index([("name", "text")])
        
        # Trash Collection Indexes
        await self.db[COLLECTIONS['trash']].create_index([("chat_id", 1), ("msg_id", 1)])
        await self.db[COLLECTIONS['trash']].create_index([("status", 1)])
        await self.db[COLLECTIONS['trash']].create_index([("moved_at", -1)])
        await self.db[COLLECTIONS['trash']].create_index([("verified_by_admin", 1)], sparse=True)
        await self.db[COLLECTIONS['trash']].create_index([("reason", 1)])

mongo = Database()