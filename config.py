import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN がありません")
if not CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID がありません")

CHAT_ID = int(CHAT_ID)

GOMINING_ACCESS_TOKEN = os.getenv("GOMINING_ACCESS_TOKEN")
GOMINING_REFRESH_TOKEN = os.getenv("GOMINING_REFRESH_TOKEN")

if not GOMINING_ACCESS_TOKEN:
    raise ValueError("GOMINING_ACCESS_TOKEN がありません")
if not GOMINING_REFRESH_TOKEN:
    raise ValueError("GOMINING_REFRESH_TOKEN がありません")

GOMINING_BASE = "https://api.gomining.com/v1"
