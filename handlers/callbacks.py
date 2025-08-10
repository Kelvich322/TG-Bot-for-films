from handlers.message_handlers import menu
from states.states import FilmStates, MainStates
from utils.kpoisk_films import (
    genre_and_year_select,
    request_films,
    give_url,
    get_random_film,
)


def register_callbacks(bot):
    @bot.callback_query_handler(func=lambda callback: callback.data == "menu")
    def callback_in_menu(callback):
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        bot.answer_callback_query(callback.id)
        bot.set_state(user_id, MainStates.menu, chat_id)
        bot.clear_step_handler_by_chat_id(chat_id)
        menu(bot, callback.message)

    @bot.callback_query_handler(func=lambda callback: callback.data == "again")
    def callback_again(callback):
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        bot.answer_callback_query(callback.id)
        bot.set_state(user_id, FilmStates.genre.name, chat_id)
        genre_and_year_select(bot, callback.message)

    @bot.callback_query_handler(func=lambda callback: callback.data == "request_film")
    def callback_yes(callback):
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        bot.answer_callback_query(callback.id)
        bot.set_state(user_id, FilmStates.request.name, chat_id)
        message = callback.message
        message.from_user.id = user_id
        request_films(bot, message)

    @bot.callback_query_handler(func=lambda callback: callback.data == "give_url")
    def callback_give_url(callback):
        user_id = callback.from_user.id
        username = callback.from_user.username
        chat_id = callback.message.chat.id
        bot.answer_callback_query(callback.id)
        bot.set_state(user_id, FilmStates.give_url.name, chat_id)
        message = callback.message
        message.from_user.id = user_id
        give_url(bot, message, username)

    @bot.callback_query_handler(func=lambda callback: callback.data == "another_film")
    def callback_another_film(callback):
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        bot.answer_callback_query(callback.id)
        bot.set_state(user_id, FilmStates.request.name, chat_id)
        bot.delete_message(chat_id, message_id=callback.message.message_id)
        bot.delete_message(chat_id, message_id=callback.message.message_id - 1)
        bot.delete_message(chat_id, message_id=callback.message.message_id - 2)
        message = callback.message
        message.from_user.id = user_id
        request_films(bot, message)

    @bot.callback_query_handler(func=lambda callback: callback.data == "random_again")
    def callback_random_again(callback):
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        bot.answer_callback_query(callback.id)
        bot.set_state(user_id, FilmStates.random_film, chat_id)
        message = callback.message
        message.from_user.id = user_id
        get_random_film(bot, message)
