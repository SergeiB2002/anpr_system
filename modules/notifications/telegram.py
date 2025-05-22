import os
from telegram import Bot
from telegram.error import TelegramError

# инициализация бота
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))


def send_alert(message: str) -> None:
    """
    Отправляет текстовое уведомление в указанный Telegram-чат.
    """
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        return
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        # Можно залогировать ошибку
        print(f"Telegram error: {e}")