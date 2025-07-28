import asyncio
import logging

from enum import Enum
from pyrogram import Client
from typing import Dict, List, Optional, Union

from config import Config
from bot.logger import LOGGER

from .utils.streamer import ByteStreamer


class BotType(Enum):
    MAIN = "main"
    WORKER = "worker"


class Bot:
    def __init__(self, bot_token: str, bot_type: BotType = BotType.WORKER, bot_id: Optional[str] = None):
        if not bot_token or not bot_token.strip():
            raise ValueError("Bot token cannot be empty")
            
        self.bot_token = bot_token
        self.bot_type = bot_type
        self.bot_id = bot_id or self._generate_bot_id(bot_token, bot_type)
        self.workload = 0
        
        self._client: Optional[Client] = None
        self._is_running = False
        
        name = self._generate_bot_name(bot_token, bot_type)
        
        client_config = self._get_client_config(name, bot_token, bot_type)
        
        try:
            self._client = Client(**client_config)
        except Exception as e:
            LOGGER.error(f"Failed to create client for bot {self.bot_id}: {e}")
            raise

        self.bytestreamer = ByteStreamer(self)
    
    def _generate_bot_id(self, bot_token: str, bot_type: BotType) -> str:
        """Generate unique bot ID"""
        if bot_type == BotType.MAIN:
            return "main_bot"
        
        import hashlib
        token_hash = hashlib.md5(bot_token.encode()).hexdigest()[:8]
        return f"worker_{token_hash}"
    
    def _generate_bot_name(self, bot_token: str, bot_type: BotType) -> str:
        """Generate a unique name for the bot"""
        if bot_type == BotType.MAIN:
            return "Project-Shizuru"
        
        import hashlib
        token_hash = hashlib.md5(bot_token.encode()).hexdigest()[:8]
        return f"bot_{token_hash}"
    
    def _get_client_config(self, name: str, bot_token: str, bot_type: BotType) -> dict:
        """Get client configuration based on bot type"""
        from config import Config
        
        base_config = {
            "name": name,
            "api_id": Config.APP_ID,
            "api_hash": Config.API_HASH,
            "bot_token": bot_token,
            "workers": 100,
            "sleep_threshold": 100,
        }
        
        if bot_type == BotType.MAIN:
            base_config.update({
                "plugins": {"root": "bot/modules"},
                "in_memory": False,
                "no_updates": False
            })
        else:
            base_config.update({
                "in_memory": True,
                "no_updates": True
            })
        
        return base_config
    
    @property
    def client(self) -> Client:
        """Get the Pyrogram client instance"""
        if self._client is None:
            raise RuntimeError("Client not initialized")
        return self._client
    
    @property
    def is_main(self) -> bool:
        """Check if this is the main bot"""
        return self.bot_type == BotType.MAIN
    
    @property
    def is_running(self) -> bool:
        """Check if bot is currently running."""
        return self._is_running and self._client and self._client.is_connected

    @property
    def is_available(self) -> bool:
        """Check if bot is available for work"""
        return self.is_running and self.workload < 100

    
    async def start(self) -> None:
        try:
            await self.client.start()
            self._is_running = True
            LOGGER.info(f"Bot {self.bot_id} started successfully")
        except Exception as e:
            LOGGER.error(f"Failed to start bot {self.bot_id}: {e}")
            self._is_running = False
            raise
    
    async def stop(self) -> None:
        try:
            if self._client and self._client.is_connected:
                await self.client.stop()
            self._is_running = False
            LOGGER.info(f"Bot {self.bot_id} stopped successfully")
        except Exception as e:
            LOGGER.error(f"Failed to stop bot {self.bot_id}: {e}")
    
    def increment_workload(self) -> None:
        """Increment workload."""
        self.workload += 1
    
    def decrement_workload(self) -> None:
        """Decrement workload"""
        self.workload = max(0, self.workload - 1)
    
    def __repr__(self) -> str:
        return f"Bot(id={self.bot_id}, type={self.bot_type.value}, workload={self.workload})"



class BotManager:
    def __init__(self):
        self._bots: Dict[str, Bot] = {}
        self._main_bot: Optional[Bot] = None
        self._worker_bots: Dict[str, Bot] = {}  # keep a seperated dict (might get usefull)
        self._is_running = False
    

    async def add_main_bot(self, bot_token: str) -> str:
        bot = Bot(bot_token, BotType.MAIN)
        self._main_bot = bot
        self._bots[bot.bot_id] = bot
        
        LOGGER.debug(f"Shizuru : Main bot added: {bot.bot_id}")
        return bot.bot_id
    

    async def add_worker_bot(self, bot_token: str, bot_id: Optional[str] = None) -> str:
        bot = Bot(bot_token, BotType.WORKER, bot_id)
        
        if bot.bot_id in self._bots:
            raise ValueError(f"Bot with ID {bot.bot_id} already exists")
        
        self._worker_bots[bot.bot_id] = bot
        self._bots[bot.bot_id] = bot
        
        LOGGER.debug(f"Shizuru : Worker bot added: {bot.bot_id}")
        return bot.bot_id
    

    async def remove_bot(self, bot_id: str) -> bool:
        """Remove a bot by ID"""
        if bot_id not in self._bots:
            return False
        
        bot = self._bots[bot_id]
        
        # Stop bot if running
        if bot.is_running:
            await bot.stop()
        
        if bot.is_main:
            self._main_bot = None
        else:
            self._worker_bots.pop(bot_id, None)
        
        self._bots.pop(bot_id, None)
        LOGGER.debug(f"Shizuru : Bot {bot_id} removed")
        return True
    

    async def start_all(self) -> None:   
        failed_bots = []
        
        for bot_id, bot in self._bots.items():
            try:
                await bot.start()
            except Exception as e:
                failed_bots.append(bot_id)

        
        self._is_running = True
        LOGGER.info(f"Bot manager started with {len(self._bots) - len(failed_bots)}/{len(self._bots)} bots")
    

    async def stop_all(self) -> None:
        if not self._is_running:
            return
        
        tasks = []
        for bot in self._bots.values():
            if bot.is_running:
                tasks.append(bot.stop())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self._is_running = False
        LOGGER.info("All bots stopped")
    

    def get_bot(self, bot_id: str) -> Optional[Bot]:
        """Get bot by ID"""
        return self._bots.get(bot_id)
    

    def get_main_bot(self) -> Optional[Bot]:
        """Get the main bot"""
        return self._main_bot

    
    def get_available_bot(self) -> Optional[Bot]:
        """Get an available worker bot with least workload"""
        available = [bot for bot in self._bots.values() if bot.is_available]
        if not available:
            return None
        # Return bot with least workload
        return min(available, key=lambda b: b.workload)
    

    def get_random_bot(self) -> Optional[Bot]:
        """Get a random available worker bot"""
        available = [bot for bot in self._bots.values() if bot.is_available]
        if not available:
            return None
        return random.choice(available)
    
    
    def get_all_bots(self) -> List[Bot]:
        """Get all bots"""
        return list(self._bots.values())


    async def __aenter__(self):
        await self.start_all()
        return self
    

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop_all()
    

    def __repr__(self) -> str:
        return f"BotManager(total={len(self._bots)})"


botmanager = BotManager()