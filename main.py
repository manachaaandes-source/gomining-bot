from telegram.ext import Updater, CommandHandler
from config import BOT_TOKEN, CHAT_ID
from gomining import GoMining
import datetime

gm = GoMining()

# /start
def start(update, context):
    context.bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "⛏ *GoMining フル管理 BOT*\n\n"
            "/help - コマンド一覧\n"
            "/status - 今日の報酬\n"
            "/reward - 報酬のみ表示\n"
            "/on - マイニングON\n"
            "/info - マイナー情報\n"
            "/power - 電力・効率\n"
            "/next_reset - 次の停止までの残り時間\n"
        ),
        parse_mode="Markdown"
    )

# /help
def help_cmd(update, context):
    start(update, context)

# /status
def status(update, context):
    reward = gm.get_daily_reward()
    btc = reward.get("amount_btc", 0)
    context.bot.send_message(chat_id=CHAT_ID, text=f"今日の報酬: {btc} BTC")

# /reward
def reward(update, context):
    reward = gm.get_daily_reward()
    btc = reward.get("amount_btc", 0)
    context.bot.send_message(chat_id=CHAT_ID, text=f"今日の報酬: {btc} BTC")

# /on
def turn_on(update, context):
    gm.mining_on()
    context.bot.send_message(chat_id=CHAT_ID, text="⛏ マイニングを再起動したよ！")

# /info
def info(update, context):
    data = gm.get_dashboard()
    
    th = data.get("hashrate_th", "?")
    efficiency = data.get("efficiency", "?")
    power = data.get("power", "?")

    msg = (
        f"📊 *マイナー情報*\n"
        f"TH: {th}\n"
        f"効率: {efficiency}%\n"
        f"電力: {power} W/TH\n"
    )

    context.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

# /power
def power(update, context):
    data = gm.get_dashboard()
    
    power = data.get("power", "?")
    efficiency = data.get("efficiency", "?")

    msg = (
        f"⚡ *電力 / 効率*\n"
        f"電力: {power} W/TH\n"
        f"効率: {efficiency}%\n"
    )
    context.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

# /next_reset
def next_reset(update, context):
    now = datetime.datetime.utcnow()
    tomorrow = now + datetime.timedelta(days=1)
    reset_time = datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0
    )
    diff = reset_time - now

    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    msg = f"⏳ 次のリセットまで {hours}時間 {minutes}分"
    context.bot.send_message(chat_id=CHAT_ID, text=msg)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("reward", reward))
    dp.add_handler(CommandHandler("on", turn_on))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("power", power))
    dp.add_handler(CommandHandler("next_reset", next_reset))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
