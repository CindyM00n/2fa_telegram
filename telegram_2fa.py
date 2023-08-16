import telebot
import pyotp
import os
from dotenv import load_dotenv

load_dotenv('/path/to/your/env/file/.env')
bot = telebot.TeleBot(os.getenv('BOT_ID'))
chat_id = int(os.getenv('CHAT_ID'))

totp_dict = {
    "gate": pyotp.TOTP(os.getenv('TOTP_GATE')),
    # "bitrue": pyotp.TOTP(os.getenv('TOTP_BITRUE')),
    # "okx": pyotp.TOTP(os.getenv('TOTP_OKX')),
    # "okx_sub1": pyotp.TOTP(os.getenv('TOTP_OKX_SUB1')),
    # "kucoin": pyotp.TOTP(os.getenv('TOTP_KUCOIN')),
    # "your_exchange_name": pyotp.TOTP(os.getenv('TOTP_exchange_name')),
}


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id == chat_id:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [name for name in totp_dict.keys()]
        keyboard.add(*buttons)

        bot.send_message(message.chat.id, 'Select cex or send your own key', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "пошел нахуй")


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.chat.id == chat_id:
        totp = totp_dict.get(message.text, pyotp.TOTP(message.text))
        formatted_text = f'`{totp.now()}`'
        bot.send_message(message.chat.id, formatted_text, disable_web_page_preview=True, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "пошел нахуй")


bot.infinity_polling()
