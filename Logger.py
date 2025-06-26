import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import RetryAfter, TelegramError

class Logger:
    def __init__(self):
        load_dotenv()
        token = os.getenv("TELEGRAM_TOKEN")
        user_id = os.getenv("TELEGRAM_USER_ID")

        if not token:
            raise ValueError("TELEGRAM_TOKEN not found in environment.")
        if not user_id:
            raise ValueError("TELEGRAM_USER_ID not found in environment.")

        self.bot = Bot(token=token)
        self.user_id = int(user_id)

    async def log(self, level: str, message: str):
        text = f"[{level.upper()}] {message}"
        try:
            await self.bot.send_message(chat_id=self.user_id, text=text)
            await asyncio.sleep(0.05)  # prevent spamming: 20 msg/sec max
            print(text)  # For testing purposes, print to console instead of sending to Telegram
        except RetryAfter as e:
            print(f"[Logger] Rate limit hit. Sleeping for {e.retry_after} seconds.")
            await asyncio.sleep(e.retry_after)
            await self.bot.send_message(chat_id=self.user_id, text=text)
        except TelegramError as e:
            print(f"[Logger Error] Telegram API error: {e}")
        except Exception as e:
            print(f"[Logger Error] Unexpected error: {e}")

    async def info(self, message: str):
        await self.log("INFO", message)

    async def error(self, message: str):
        await self.log("ERROR", message)
