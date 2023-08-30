from telegram import Bot

class TelegramBot:
    def __init__(self, api_token):
        self.api_token = api_token

    async def send_message(self, chat_id, text, parse_mode='None'):
        bot = Bot(token=self.api_token)
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)