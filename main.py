from dotenv import load_dotenv
import os
from telegram import Bot
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from telegram.ext import Updater


load_dotenv()
TOKEN = os.getenv("API_KEY")
ALLOWED_CHAT_IDS = [int(chat_id)
                    for chat_id in os.getenv("ALLOWED_CHAT_IDS").split(",")]




async def send_telegram_message(message: str):
    bot = Bot(token=TOKEN)
    for chat_id in ALLOWED_CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message)


async def main() -> None:
    await send_telegram_message(f"successful!")


asyncio.run(main())
