import logging

import requests
from decouple import config
from telegram import Update
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes)
from app.models import UserData


class TelegramBot:
    def __init__(self) -> None:
        __SECRET = config("TELEGRAM_SECRET")
        self.app = ApplicationBuilder().token(__SECRET).build()
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def get_joke(self):
        url = "https://v2.jokeapi.dev/joke/Any?type=single"
        response = requests.get(url)
        return response.json()["joke"]

    @staticmethod
    def get_markup():
        return InlineKeyboardMarkup([[
                InlineKeyboardButton("stupid", callback_data="/stupid"),
                InlineKeyboardButton("fat", callback_data="/fat")
            ], [
                InlineKeyboardButton("dumb", callback_data="/dumb"),
                InlineKeyboardButton("history", callback_data="/history")]])

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.info("Welcome %s!", update.message.from_user.first_name)
        await context.bot.sendMessage(chat_id=update.effective_chat.id, 
        text=f"Hi, {update.effective_chat.first_name}\nPlease click on any button", reply_markup=self.get_markup())

    async def callback_query_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query.data
        await context.bot.sendMessage(chat_id=update.effective_chat.id, 
            text=self.get_joke(), reply_markup=self.get_markup())
        
        # Save User HISTORY
        obj, is_created = UserData.objects.get_or_create(
            id=update.effective_user.id,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )

        if query == "/stupid":
            obj.stupid_btn += 1
        if query == "/fat":
            obj.fat_btn += 1
        if query == "/dumb":
            obj.dumb_btn += 1
        if query == "/history":
            get_objs = UserData.objects.filter(id=update.effective_user.id)
            if get_objs.exists():
                history = f"Hello, {get_objs[0].first_name} {get_objs[0].last_name}\nJokes count History!\n\nstupd: {get_objs[0].stupid_btn}\nfat: {get_objs[0].fat_btn}\ndumb: {get_objs[0].dumb_btn}"
            else:
                history = "No history found!"
            await context.bot.sendMessage(chat_id=update.effective_chat.id, text=history)

        obj.save()
        return query

    def run_bot(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.callback_query_handler))
        self.app.run_polling()

    def stop_bot(self):
        self.app.shutdown()


if __name__ == "__main__":
    obj = TelegramBot()
    obj.run_bot()