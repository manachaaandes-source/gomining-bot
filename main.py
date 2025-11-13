import os
import requests
from telegram.ext import Updater, CommandHandler
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GOMINING_ACCESS_TOKEN = os.getenv("GOMINING_ACCESS_TOKEN")
GOMINING_REFRESH_TOKEN = os.getenv("GOMINING_REFRESH_TOKEN")

BASE = "https://api.gomining.com/v1"


# ============================
# GoMining API Helper
# ============================

def headers():
    return {
        "Authorization": f"Bearer {GOMINING_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }


def get_miner():
    res = requests.get(f"{BASE}/mining/my_minings", headers=headers()).json()
    if not res or "data" not in res:
        return None
    return res["data"][0]


def turn_on_mining(miner_id):
    data = {"command": "start"}
    r = requests.post(f"{BASE}/mining/{miner_id}/action", json=data, headers=headers())
    return r.status_code == 200


def fetch_reward_history(days=7):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    params = {
        "from": start_date.strftime("%Y-%m-%dT00:00:00Z"),
        "to": end_date.strftime("%Y-%m-%dT23:59:59Z"),
        "limit": 50,
        "offset": 0
    }

    r = requests.get(f"{BASE}/wallet/transactions", params=params, headers=headers())
    if r.status_code != 200:
        return None

    tx = r.json().get("data", [])
    result = [t for t in tx if t.get("type") == "mining_reward"]
    return result


# ============================
# Telegram Commands
# ============================

def start(update, context):
    msg = (
        "⛏ GoMining フル管理BOT\n\n"
        "/status - 今日の報酬\n"
        "/reward - 報酬額だけ表示\n"
        "/info - マイナー情報\n"
        "/power - 電力と効率\n"
        "/on - マイニング強制ON\n"
        "/auto_fix - 止まってたら自動ON\n"
        "/history - 収益履歴\n"
        "/predict - 収益予測\n"
    )
    context.bot.send_message(chat_id=CHAT_ID, text=msg)


def status(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="データ取得失敗")
        return

    reward = miner["userReward"]["btc"]
    usd = miner["userReward"]["usd"]
    eff = miner["mineEfficiency"]
    th = miner["hashrate"]

    text = (
        f"今日の報酬\n"
        f"BTC: {reward}\n"
        f"USD: {usd}\n\n"
        f"効率: {eff}\n"
        f"ハッシュ: {th} TH\n"
    )
    context.bot.send_message(chat_id=CHAT_ID, text=text)


def reward(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="エラー")
        return

    context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"今日の報酬: {miner['userReward']['btc']} BTC"
    )


def info(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="取得失敗")
        return

    text = (
        f"マイナー情報\n"
        f"TH/s: {miner['hashrate']}\n"
        f"効率: {miner['mineEfficiency']}\n"
        f"消費電力: {miner['powerConsumption']}\n"
    )
    context.bot.send_message(chat_id=CHAT_ID, text=text)


def power(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="エラー")
        return

    text = (
        f"電力詳細\n"
        f"消費電力: {miner['powerConsumption']} W\n"
        f"効率: {miner['mineEfficiency']}\n"
    )
    context.bot.send_message(chat_id=CHAT_ID, text=text)


def on(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="取得エラー")
        return

    if turn_on_mining(miner["id"]):
        context.bot.send_message(chat_id=CHAT_ID, text="マイニングONしました！")
    else:
        context.bot.send_message(chat_id=CHAT_ID, text="ON失敗")


# ============================
# auto_fix：止まってたらON
# ============================

def auto_fix(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="Miner取得失敗")
        return

    if miner["isMining"]:
        context.bot.send_message(chat_id=CHAT_ID, text="稼働中！問題なし👌")
        return

    ok = turn_on_mining(miner["id"])
    if ok:
        context.bot.send_message(chat_id=CHAT_ID, text="停止を検知 → マイニングONに復旧しました！")
    else:
        context.bot.send_message(chat_id=CHAT_ID, text="復旧失敗…")


# ============================
# /history：報酬履歴
# ============================

def history(update, context):
    data = fetch_reward_history(days=7)

    if not data:
        context.bot.send_message(chat_id=CHAT_ID, text="履歴取得できませんでした")
        return

    msg = "過去7日の報酬\n\n"
    for tx in data:
        date = tx["createdAt"].split("T")[0]
        btc = tx["amount"]["btc"]
        usd = tx["amount"]["usd"]
        msg += f"{date} → {btc} BTC / ${usd}\n"

    context.bot.send_message(chat_id=CHAT_ID, text=msg)


# ============================
# /predict：収益予測
# ============================

def predict(update, context):
    miner = get_miner()
    if not miner:
        context.bot.send_message(chat_id=CHAT_ID, text="エラー")
        return

    daily = float(miner["userReward"]["btc"])  # 1日の報酬（現在の状態）

    text = (
        "収益予測\n\n"
        f"1日 → {daily} BTC\n"
        f"30日 → {daily * 30} BTC\n"
        f"365日 → {daily * 365} BTC\n"
    )

    context.bot.send_message(chat_id=CHAT_ID, text=text)


# ============================
# BOT起動
# ============================

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("reward", reward))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("power", power))
    dp.add_handler(CommandHandler("on", on))
    dp.add_handler(CommandHandler("auto_fix", auto_fix))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(CommandHandler("predict", predict))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
