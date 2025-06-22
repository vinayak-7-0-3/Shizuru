import asyncio
import base64

from aiohttp import ClientSession
from typing import Optional, Dict, Any, List

from ..utils.errors import SpotifyError


class SpotifyAPI:
    def __init__(self, session: ClientSession, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.spotify.com/v1"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.access_token = None
        self.session = session

    
    async def _get_access_token(self) -> None:
        """Get access token using client credentials flow"""
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("ascii")
        auth_base64 = base64.b64encode(auth_bytes).decode("ascii")
        
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        async with self.session.post(self.token_url, headers=headers, data=data) as response:
            if response.status == 200:
                token_data = await response.json()
                self.access_token = token_data["access_token"]
            else:
                raise SpotifyError(f"Failed to get access token: {response.status}")
    
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """Make authenticated request to Spotify API"""
        if not self.access_token:
            await self._get_access_token()
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.base_url}/{endpoint}"
        
        async with self.session.get(url, headers=headers, params=params) as response:
            if response.status == 401:  # Token expired
                await self._get_access_token()
                headers = {"Authorization": f"Bearer {self.access_token}"}
                async with self.session.get(url, headers=headers, params=params) as retry_response:
                    return await retry_response.json()
            elif response.status == 200:
                return await response.json()
            else:
                raise SpotifyError(f"API request failed: {response.status}")
    
    async def search(self, title: str, artist: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for tracks by title and artist"""
        query = f"track:{title} artist:{artist}"
        params = {
            "q": query,
            "type": "track",
            "limit": limit
        }
        
        response = await self._make_request("search", params)
        return response.get("tracks", {}).get("items", [])
    
    async def get_album(self, album_id: str) -> Dict[str, Any]:
        """Get album by ID"""
        return await self._make_request(f"albums/{album_id}")
    
    async def get_artist(self, artist_id: str) -> Dict[str, Any]:
        """Get artist by ID"""
        return await self._make_request(f"artists/{artist_id}")