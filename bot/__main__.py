import asyncio

from pyrogram import idle

from config import Config
from .tgclient import botmanager
from .database.connection import mongo
from .logger import LOGGER
from .metadata.handler import meta_manager


async def main():
    main_bot = await botmanager.add_main_bot(Config.TG_BOT_TOKEN)
    if Config.MULTI_CLIENTS:
        for token in Config.MULTI_CLIENTS:
            await botmanager.add_worker_bot(token)
    
    await botmanager.start_all()
    await mongo.connect()
    await meta_manager.setup()

    await idle()

    await meta_manager.stop()
    await mongo.disconnect()
    await botmanager.stop_all()

if __name__ == '__main__':
    asyncio.run(main())