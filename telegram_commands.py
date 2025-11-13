from gomining import GoMining
from telegram import Update
from telegram.ext import ContextTypes

gm = GoMining()

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⛏ GoMining 完全BOT\n"
        "/status → ステータス\n"
        "/on → マイニングON\n"
        "/reward → 今日の報酬\n"
    )
    await update.message.reply_text(text)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reward = gm.get_daily_reward()
    btc = reward.get("amount_btc", 0)

    text = (
        f"⛏ ステータス\n"
        f"今日の報酬: {btc} BTC\n"
        f"マイニング: 常時ON（6時間更新制）\n"
    )
    await update.message.reply_text(text)


async def cmd_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reward = gm.get_daily_reward()
    btc = reward.get("amount_btc", 0)
    await update.message.reply_text(f"今日の報酬: {btc} BTC")


async def cmd_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = gm.mining_on()
    await update.message.reply_text("🔄 マイニングONにしたよ！")
