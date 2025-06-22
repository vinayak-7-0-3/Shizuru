from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Tuple
from pyrogram.enums import MessageMediaType

from ..utils.queue import AsyncQueueProcessor
from ..metadata.handler import meta_manager
from ..database import AlbumManager, ArtistManager, TrackManager

async def handle_tracks(data: Tuple[Client, Message]):
    c, msg = data

    if msg.media == MessageMediaType.AUDIO:
        audio_data = msg.audio
        
        title = audio_data.title
        artist = audio_data.performer

        metadata = await meta_manager.search(title, artist)

        metadata.chat_id = msg.chat.id
        metadata.msg_id = msg.id
        metadata.file_unique_id = audio_data.file_unique_id
        metadata.mime_type = audio_data.mime_type
        metadata.file_size = audio_data.file_size


        song_exist = await TrackManager.check_exists(
            metadata.track_id, metadata.file_unique_id
        )

        if song_exist:
            return

        await TrackManager.insert_track(metadata)

        artist_exist = await ArtistManager.check_exists(
            metadata.artist_id, metadata.artist
        )
        if not artist_exist:
            artist_data = await meta_manager.get_artist(
                metadata.artist_id, metadata.artist
            )
            await ArtistManager.insert_artist(artist_data)
        
        if metadata.album_id:
            album_exist = await AlbumManager.check_album_exists(metadata.album_id)
            if not album_exist:
                album_data = await meta_manager.get_album(metadata.album_id)
                await AlbumManager.insert_album(album_data)


processor = AsyncQueueProcessor(handle_tracks)

@Client.on_message(filters.audio | filters.document)
async def handle_music(c: Client, msg: Message):
    await processor.add_item((c, msg))