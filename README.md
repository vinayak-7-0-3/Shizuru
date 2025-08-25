
# Shizuru-Backend
![GitHub Repo stars](https://img.shields.io/github/stars/vinayak-7-0-3/Shizuru-Backend?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/vinayak-7-0-3/Shizuru-Backend?style=for-the-badge)
![Docker Pulls](https://img.shields.io/docker/pulls/weebzbots/shizuru-backenda?style=for-the-badge)
[![Static Badge](https://img.shields.io/badge/support-pink?style=for-the-badge)](https://t.me/weebzgroup)

Backend service for **Shizuru**.  
Built with **FastAPI + MongoDB + Pyrogram**

Note: This is not a Voice Chat Music Streaming Bot

## FEATURES

**Currently the project is in early development stage and features are incomplete**

Feels free to check the repo and report bugs / features

## INSTALLATION


#### 1) LOCAL DEPLOYMENT

**Requirements**
- Python>=3.10 (3.12 recommended) 
- Git installed (optional)

**Steps**
- Git clone (or download) the repo
- Create virtual environment and run
```
virtualenv -p python3 VENV
. ./VENV/bin/activate
```
- Edit and fill out the essentials environment variables in `sample.env` (refer [here](#variables-info))
- Rename `sample.env` to `.env`
- Finally run
```
pip install -r requirements.txt
python -m bot
```

## VARIABLES INFO

#### ESSENTIAL VARIABLES
- `TG_BOT_TOKEN` - Telegeam bot token (get it from [BotFather](https://t.me/BotFather))
- `APP_ID` - Your Telegram APP ID (get it from my.telegram.org) `(int)`
- `API_HASH` - Your Telegram APP HASH (get it from my.telegram.org) `(str)`
- `DATABASE_URL` - MongoDB database URL (self hosted or atlas) `(str)`
- `DATABASE_NAME` - MongoDB database name `(str)`
- `BOT_USERNAME` - Your Telegram Bot username (with or without `@`) `(str)`
- `ADMINS` - List of Admin users for the Bot (seperated by space) `(str)`
- `MUSIC_CHANNELS` - List of music channel ID for indexing files (seperated by space) `(str)`
- `SECRET_KEY` - Just some random string (you need this also in Frontend) `(str)`

#### OPTIONAL VARIABLES
- `MULTI_CLIENTS` - List of bot tokens (eg: ["6565575:asaca", "5645654:sdfsdf"]) `(str)`
- `METADATA_PROVIDER` - Which provider to use for fetching metadata (default: spotify) `(str)`
- `SPOTIFY_CLIENT` - Client ID of Spotify App (only needed if metadata provider is set to spotify)`(str)`
- `SPOTIFY_SECRET` - Client Secret of Spotify App (only needed if metadata provider is set to spotify `(str)`

## CREDITS
- TechZIndex - https://github.com/TechShreyash/TechZIndex
- Surf-TG - https://github.com/weebzone/Surf-TG
- reelnn-backend - https://github.com/rafsanbasunia/reelnn-backend

## Support Me ❤️
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I7FWQZ4)

TON - `UQBBPkWSnbMWXrM6P-pb96wYxQzLjZ2hhuYfsO-N2pVmznCG`
