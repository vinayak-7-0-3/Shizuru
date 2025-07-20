from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ..database.connection import mongo
from ..database.models import DBTrack, DBArtist, DBAlbum
from ..utils.pagination import paginate

router = APIRouter()

@router.get("/songs", response_model=List[DBTrack])
async def get_songs(limit: int = 10, page: int = 1):
    paging = paginate(limit, page)
    cursor = mongo.db["songs"].find().skip(paging["skip"]).limit(paging["limit"])
    results = [DBTrack(**song) async for song in cursor]
    return results

@router.get("/songs/{id}", response_model=DBTrack)
async def get_song(id: str):
    song = await mongo.db["songs"].find_one({"track_id": id})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return DBTrack(**song)

@router.get("/artists", response_model=List[DBArtist])
async def get_artists(limit: int = 10, page: int = 1):
    paging = paginate(limit, page)
    cursor = mongo.db["artists"].find().skip(paging["skip"]).limit(paging["limit"])
    results = [DBArtist(**artist) async for artist in cursor]
    return results

@router.get("/artists/{id}", response_model=DBArtist)
async def get_artist(id: str):
    artist = await mongo.db["artists"].find_one({"artist_id": id})
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return DBArtist(**artist)

@router.get("/albums", response_model=List[DBAlbum])
async def get_albums(limit: int = 10, page: int = 1):
    paging = paginate(limit, page)
    cursor = mongo.db["albums"].find().skip(paging["skip"]).limit(paging["limit"])
    results = [DBAlbum(**album) async for album in cursor]
    return results

@router.get("/albums/{id}", response_model=DBAlbum)
async def get_album(id: str):
    album = await mongo.db["albums"].find_one({"album_id": id})
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return DBAlbum(**album)
