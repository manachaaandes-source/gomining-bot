import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN
from telegram_commands import cmd_start, cmd_status, cmd_reward, cmd_on

app = FastAPI()

BOT_URL = os.getenv("BOT_WEBHOOK_URL")

application = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

application.add_handler(CommandHandler("start", cmd_start))
application.add_handler(CommandHandler("status", cmd_status))
application.add_handler(CommandHandler("reward", cmd_reward))
application.add_handler(CommandHandler("on", cmd_on))

@app.post("/")
async def telegram_webhook(request: Request):
    json_data = await request.json()
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return "ok"

@app.on_event("startup")
async def on_startup():
    await application.bot.set_webhook(url=BOT_URL)

