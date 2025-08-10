import telebot

from config.API_config import BotSettings
from handlers.callbacks import register_callbacks
from handlers.command_handlers import register_command_handlers
from handlers.message_handlers import register_message_handlers
from models.database import init_db


init_db()
bot_token = BotSettings()

bot = telebot.TeleBot(bot_token.token.get_secret_value())

register_command_handlers(bot)
register_message_handlers(bot)
register_callbacks(bot)


bot.infinity_polling()
