import asyncio
import json
from channels.generic.websocket import WebsocketConsumer
from app.telegram_bot import TelegramBot


class TelegramConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({"message": "Connected... !"}))

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data):
        res = json.loads(text_data)
        cmd = res.get("message")

        if cmd == "start-bot":
            self.send(text_data=json.dumps({"message": "Telegram bot started!"}))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            bot = TelegramBot()
            bot.run_bot()

        if cmd == "stop-bot":
            bot.stop_bot()
            self.send(text_data=json.dumps({"message": "Telegram bot stoped!"}))