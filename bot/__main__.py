import signal
import asyncio

import uvicorn
from uvicorn import Config as UvicornConfig, Server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyrogram import idle

from config import Config
from .tgclient import botmanager
from .database.connection import mongo
from .logger import LOGGER
from .metadata.handler import meta_manager
from .server.routes import router


web_server = FastAPI(title="Shizuru Backend API")
web_server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
web_server.include_router(router)

shutdown_event = asyncio.Event()

def _signal_handler():
    LOGGER.info("🔴 Shutdown signal received...")
    shutdown_event.set()


async def run_fastapi():
    config = uvicorn.Config(app=web_server, host="0.0.0.0", port=8501, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    main_bot = await botmanager.add_main_bot(Config.TG_BOT_TOKEN)
    if Config.MULTI_CLIENTS:
        for token in Config.MULTI_CLIENTS:
            await botmanager.add_worker_bot(token)
    
    await botmanager.start_all()
    await mongo.connect()
    await meta_manager.setup()

    await asyncio.gather(
        run_fastapi(),
        shutdown_event.wait()  # Wait for signal
    )


    await meta_manager.stop()
    await mongo.disconnect()
    await botmanager.stop_all()

if __name__ == '__main__':
    asyncio.run(main())