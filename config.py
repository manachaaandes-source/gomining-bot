import os

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("環境変数 TELEGRAM_BOT_TOKEN が設定されていません！")

if not CHAT_ID:
    raise ValueError("環境変数 TELEGRAM_CHAT_ID が設定されていません！")

# CHAT_ID を整数に変換（重要）
CHAT_ID = int(CHAT_ID)

# GoMining
GOMINING_ACCESS_TOKEN = os.getenv("GOMINING_ACCESS_TOKEN")
GOMINING_REFRESH_TOKEN = os.getenv("GOMINING_REFRESH_TOKEN")

if not GOMINING_ACCESS_TOKEN:
    raise ValueError("環境変数 GOMINING_ACCESS_TOKEN が設定されていません！")

if not GOMINING_REFRESH_TOKEN:
    raise ValueError("環境変数 GOMINING_REFRESH_TOKEN が設定されていません！")

GOMINING_BASE = "https://api.gomining.com/v1"
