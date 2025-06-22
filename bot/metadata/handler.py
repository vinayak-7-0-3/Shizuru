from aiohttp import ClientSession

from .amp import AppleMusic
from .spotify import SpotifyAPI
from .models import *
from config import Config
from bot.logger import LOGGER

class MetadataManager:
    session: ClientSession
    def __init__(self):
        self.client = None
        self.session = None
        self.provider = Config.METADATA_PROVIDER


    async def setup(self) -> None:
        """Initialise the necessary clients"""
        self.session = ClientSession()
        if self.provider == 'apple-music':
            self.client = AppleMusic(self.session)
        else:
            self.client = SpotifyAPI(self.session, Config.SPOTIFY_CLIENT, Config.SPOTIFY_TOKEN)


    async def search(self, title: str, artist: str) -> BaseTrack:
        """Get track details from query"""
        try:
            result = await self.client.search(f"{title} {artist}")
            return result
        except Exception as e:
            LOGGER.error(e)
            LOGGER.debug("MetadataManager : Falling back to telegram metadata")
            return BaseTrack(
                title=title, artist=artist, provider='null'
            )


    async def get_artist(self, artist_id: str, artist_name: str) -> BaseArtist:
        try:
            assert(artist_id)
            result = await self.client.get_artist(artist_id)
            return result
        except Exception as e:
            LOGGER.error(e)
            return BaseArtist(
                name=artist_name,
                provider='null'
            )

    
    async def get_album(self, album_id: str) -> BaseAlbum:
        try:
            result = await self.client.get_album(album_id)
            return result
        except Exception as e:
            LOGGER.error(e)
            return None


    async def stop(self):
        await self.session.close()


meta_manager = MetadataManager()
