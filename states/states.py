import telebot
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

from config.API_config import BotSettings

storage = StateMemoryStorage()
bot_token = BotSettings()
bot = telebot.TeleBot(bot_token.token.get_secret_value())


class FilmStates(StatesGroup):
    genre = State()
    year = State()
    request = State()
    get_film = State()
    give_url = State()
    random_film = State()


class MainStates(StatesGroup):
    menu = State()
    viewed_materials = State()
