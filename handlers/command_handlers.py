from models.users import create_user
from keyboards.ReplyKeyboards.ReplyKeyboards import keyboard_to_start
from states.states import MainStates


def start(bot, message):
    user_name = message.from_user.first_name
    user_login = message.from_user.username
    bot.send_message(
        message.chat.id,
        f"Привет, {user_name}! 👋\nЯ бот для лёгкого выбора фильма на вечер🤖\n\n"
        f"Со мной ты можешь:\n\n"
        f"1. Найти случайно фильмы, выбрав год выпуска и жанр 🎞  \n"
        f"2. Выбрать из топа случайный фильм, если вообще не знаешь что посмотреть. ⭐️\n\n"
        f"Давай начнём! Выбери нужную кнопку на клавиатуре снизу ⬇️",
        reply_markup=keyboard_to_start(),
    )
    bot.set_state(message.from_user.id, MainStates.menu.name, message.chat.id)
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {MainStates.menu}"
    )
    create_user(user_login, user_name)


def register_command_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start_handler(message):
        start(bot, message)
