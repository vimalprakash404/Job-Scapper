# logger.py
import os
from dotenv import load_dotenv
from telegram import Bot

class Logger:
    def __init__(self):
        load_dotenv()  # Load .env variables
        token = os.getenv("TELEGRAM_TOKEN")
        user_id = os.getenv("TELEGRAM_USER_ID")

        if not token:
            raise ValueError("TELEGRAM_TOKEN not found in environment.")
        if not user_id:
            raise ValueError("LOGGER_USER_ID not found in environment.")

        self.bot = Bot(token=token)
        self.user_id = int(user_id)

    async def info(self, message: str):
        try:
            await self.bot.send_message(chat_id=self.user_id, text=message)
        except Exception as e:
            print(f"[Logger Error] Failed to send log: {e}")

    async def info(self, message: str):
        try:
            await self.bot.send_message(chat_id=self.user_id, text=message)
        except Exception as e:
            print(f"[Logger Error] Failed to send log: {e}")
