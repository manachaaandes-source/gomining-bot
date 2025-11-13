import time
from gomining import GoMiningClient
from telegram_bot import send_message

gm = GoMiningClient()

def main_loop():
    while True:
        try:
            reward = gm.get_daily_reward()

            btc = reward.get("amount_btc", 0)
            usd = reward.get("amount_usd", 0)

            msg = (
                f"🟣 GoMining 今日の報酬\n"
                f"BTC: {btc}\n"
                f"USD: ${usd}\n\n"
                f"⛏ マイニングを自動でONにします..."
            )
            send_message(msg)

            gm.enable_mining_mode()
            send_message("✅ マイニング 再稼働完了！")

        except Exception as e:
            send_message(f"⚠ エラー発生: {e}")

        time.sleep(24 * 60 * 60)  # 24時間
        # テストしたいときは 60秒に変更

if __name__ == "__main__":
    main_loop()
