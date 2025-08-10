from keyboards.InlineKeyboards.InlineKeyboards import return_in_menu_markup
from keyboards.ReplyKeyboards.ReplyKeyboards import keyboard_to_start, remove_markup
from models.viewed import get_viewed_materials
from states.states import MainStates, FilmStates
from utils.kpoisk_films import genre_and_year_select, get_random_film


def menu(bot, message):
    bot.send_message(
        message.chat.id,
        f"Выбери нужную кнопку на клавиатуре снизу ⬇️",
        reply_markup=keyboard_to_start(),
    )
    bot.set_state(message.from_user.id, MainStates.menu.name, message.chat.id)
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {MainStates.menu}"
    )


def viewed_materials(bot, message):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {MainStates.menu}"
    )
    if not (
        bot.get_state(message.from_user.id, message.chat.id) == MainStates.menu.name
    ) or (
        bot.get_state(message.from_user.id, message.chat.id)
        == MainStates.viewed_materials.name
    ):
        print("Функция не прошла проверку")
        return

    bot.set_state(
        message.from_user.id, MainStates.viewed_materials.name, message.chat.id
    )

    bot.send_message(
        message.chat.id,
        "Вот фильмы, которые вы смотрели:",
        reply_markup=remove_markup(),
    )

    materials = get_viewed_materials(message.from_user.username)
    stroke = ""

    for i, material in enumerate(materials):
        formatted_date = material.date.strftime("%d.%m.%Y")
        stroke += (
            f"{i + 1}. "
            f"Название: {material.material_name} | "
            f"<a href='{material.material_url}'>Ссылка</a> | "
            f"Дата: {formatted_date}\n\n"
        )

    bot.send_message(
        message.chat.id, stroke, reply_markup=return_in_menu_markup(), parse_mode="HTML"
    )


def random_film(bot, message):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {MainStates.menu}"
    )
    if not (
        bot.get_state(message.from_user.id, message.chat.id) == MainStates.menu.name
    ) or (
        bot.get_state(message.from_user.id, message.chat.id)
        == FilmStates.random_film.name
    ):
        print("Функция не прошла проверку")
        return

    bot.set_state(message.from_user.id, FilmStates.random_film.name, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"Выбираю для вас случайный фильм из лучших фильмов Кинопоиска 🔜",
        reply_markup=remove_markup(),
    )
    get_random_film(bot, message)


def register_message_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "Выбрать фильм")
    def handle_film_selection(message):
        genre_and_year_select(bot, message)

    @bot.message_handler(func=lambda message: message.text == "История просмотра")
    def viewed_mats(message):
        viewed_materials(bot, message)

    @bot.message_handler(func=lambda message: message.text == "Выбрать случайный фильм")
    def random_film_handler(message):
        random_film(bot, message)
