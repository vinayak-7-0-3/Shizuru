import os
from os import getenv
from dotenv import load_dotenv

import json
from typing import List

if not os.environ.get("ENV"):
    load_dotenv('.env', override=True)

class Config(object):
    try:
        TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
        APP_ID = int(getenv("APP_ID"))
        API_HASH = getenv("API_HASH")

        DATABASE_URL = getenv("DATABASE_URL")
        DATABASE_NAME = getenv("DATABASE_NAME")

        BOT_USERNAME = getenv("BOT_USERNAME")
        ADMINS = set(int(x) for x in getenv("ADMINS").split())
        MUSIC_CHANNELS = set(int(x) for x in getenv("MUSIC_CHANNELS").split())

        PORT = int(getenv('PORT', 8080))

        SPOTIFY_CLIENT = getenv("SPOTIFY_CLIENT")
        SPOTIFY_SECRET = getenv("SPOTIFY_SECRET")
    except:
        print("BOT : Essential Configs are missing")
        exit(1)

    MULTI_CLIENTS = getenv("MULTI_CLIENTS", None) # example '["token1", "token2", "token3"]'
    METADATA_PROVIDER = getenv("METADATA_PROVIDER", 'apple-music')



    # Do not touch (except for yk what you doin)
    if MULTI_CLIENTS:
        try:
            MULTI_CLIENTS = json.loads(MULTI_CLIENTS)
        except json.JSONDecodeError:
            print("CRITICAL: Invalid JSON in MULTI_CLIENTS")
            MULTI_CLIENTS = None