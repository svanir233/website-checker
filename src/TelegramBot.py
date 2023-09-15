from telegram import Bot
import telegram.error
import asyncio

class TelegramBot:
    def __init__(self, api_token, retry_limit=3):
        self.api_token = api_token
        self.retry_limit = retry_limit

    async def send_message(self, chat_id, text, parse_mode='None'):
        bot = Bot(token=self.api_token)
        retry_count = 0

        while retry_count < self.retry_limit:
            try:
                await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
                return  # Exit the loop if the message is sent successfully
            except Exception as e:
                print(f"Telegram API request timed out: {e}")
                retry_count += 1
                if retry_count < self.retry_limit:
                    await asyncio.sleep(10)  # Wait for 10 seconds before retrying
                else:
                    print("Retry limit reached, giving up on sending the message")
                    break