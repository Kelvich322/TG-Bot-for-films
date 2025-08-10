import random
import traceback

import requests

from config.API_config import KpoiskSettings
from keyboards.InlineKeyboards.InlineKeyboards import (
    return_in_menu_markup,
    yes_or_again_markup,
    under_film_markup,
    again_markup,
    under_random_film,
)
from keyboards.ReplyKeyboards.ReplyKeyboards import remove_markup
from models.viewed import add_viewed_material
from states.states import FilmStates, MainStates


genres = [
    {"genre": "триллер", "id": 1},
    {"genre": "драма", "id": 2},
    {"genre": "криминал", "id": 3},
    {"genre": "мелодрама", "id": 4},
    {"genre": "детектив", "id": 5},
    {"genre": "фантастика", "id": 6},
    {"genre": "приключения", "id": 7},
    {"genre": "боевик", "id": 11},
    {"genre": "фэнтези", "id": 12},
    {"genre": "комедия", "id": 13},
    {"genre": "ужасы", "id": 17},
    {"genre": "мультфильм", "id": 18},
]


def genre_and_year_select(bot, message):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {MainStates.menu}"
    )
    global genres
    genres_for_user = [i["genre"].title() for i in genres]
    bot.send_message(
        message.chat.id,
        f"Отлично! Давайте выберем жанр и год выпуска фильма, который вы бы хотели посмотреть.\n"
        f"После введения данных я найду для вас случайные 5 фильмов, подходящие под ваш запрос.\n\n"
        f"Cписок доступных жанров:\n\n•"
        f"{'\n•'.join(genres_for_user)}\n\n",
        reply_markup=remove_markup(),
    )
    bot.send_message(
        message.chat.id,
        f"Введите название жанра, который вам нравится.",
        reply_markup=return_in_menu_markup(),
    )
    bot.set_state(message.from_user.id, FilmStates.genre.name, message.chat.id)
    bot.register_next_step_handler(message, process_genre_selection, bot)


def process_genre_selection(message, bot):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {FilmStates.genre}"
    )
    if (
        not bot.get_state(message.from_user.id, message.chat.id)
        == FilmStates.genre.name
    ):
        return

    global genres
    user_genre = message.text.lower()
    genre_id = list(filter(lambda x: x["genre"] == user_genre, genres))

    try:
        if genre_id == []:
            raise TypeError

        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["genre"] = genre_id[0]["genre"]
                data["genre_id"] = genre_id[0]["id"]
            bot.reply_to(
                message, f"Отлично. Вы выбрали жанр: {genre_id[0]['genre'].title()}"
            )
            bot.set_state(message.from_user.id, FilmStates.year.name, message.chat.id)
            bot.send_message(
                message.chat.id,
                f"Теперь давайте выберем год. Введите год от 1900 до 2025.",
                reply_markup=return_in_menu_markup(),
            )
            bot.register_next_step_handler(message, process_year_selection, bot)

    except TypeError:
        bot.reply_to(
            message,
            "Некорректный жанр, пожалуйста, введите жанр из списка.",
            reply_markup=return_in_menu_markup(),
        )
        bot.register_next_step_handler(message, process_genre_selection, bot)


def process_year_selection(message, bot):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {FilmStates.genre}"
    )
    if not bot.get_state(message.from_user.id, message.chat.id) == FilmStates.year.name:
        return

    try:
        user_year = int(message.text)
        if user_year > 2025 or user_year < 1895:
            raise ValueError

        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["year"] = user_year
                genre = data.get("genre", "не указан")
                genre_id = data.get("genre_id", "не указан")
                year = data["year"]
            bot.set_state(
                message.from_user.id, FilmStates.request.name, message.chat.id
            )
            bot.reply_to(
                message,
                f"Отлично! Ваш выбор:\n"
                f"Жанр: {genre.title()}\n"
                f"Год: {year}\n\n"
                f"Всё верно?",
                reply_markup=yes_or_again_markup(),
            )

    except ValueError:
        bot.reply_to(
            message,
            "Некорректный ввод. Пожалуйста, введите год от 1900 до 2025.",
            reply_markup=return_in_menu_markup(),
        )
        bot.register_next_step_handler(message, process_year_selection, bot)


def request_films(bot, message):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {FilmStates.request}"
    )
    if (
        not bot.get_state(message.from_user.id, message.chat.id)
        == FilmStates.request.name
    ):
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        year = data.get("year", "не указан")
        genre_id = data.get("genre_id", "не указан")

    kpoisk_api = KpoiskSettings()
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films"
    headers = {
        "X-API-KEY": kpoisk_api.api.get_secret_value(),
        "Content-Type": "application/json",
    }
    params = {
        "genres": genre_id,
        "order": "RATING",
        "type": "FILM",
        "yearFrom": year,
        "yearTo": year,
        "page": 1,
        "notNullFields": "nameRu,posterUrl,description,year",
        "isStrict": "true",
        "excludeGenres": "24",
        "excludeCountries": "Япония",  # Дополнительно исключаем японские фильмы
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        films = response.json().get("items", [])
        filtered_films = [
            film
            for film in films
            if not any(g["genre"] in ["аниме"] for g in film.get("genres", []))
            and film.get("countries", [{}])[0].get("country") != "Япония"
            and film.get("nameRu") is not None
        ]  # Убираю Аниме из поиска, т.к. даже через params они не фильтруются и убираю фильмы с пустым названием и описанием

        if not films:
            bot.send_message(
                message.chat.id,
                "По вашему запросу ничего не найдено.",
                reply_markup=return_in_menu_markup(),
            )
            return
        random_films = random.sample(filtered_films, min(5, len(filtered_films)))
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["films"] = random_films

        films_list = "\n".join(
            f"{i + 1}. {film['nameRu']}" for i, film in enumerate(random_films)
        )

        bot.send_message(
            message.chat.id,
            f"По вашему запросу найдены фильмы:"
            f"\n\n{films_list}\n\n"
            "Введите номер понравившегося фильма.",
            reply_markup=again_markup(),
        )
        bot.register_next_step_handler(message, get_film, bot)

    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Ошибка при запросе к API: {e}\n{error_traceback}")
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при поиске фильмов.",
            reply_markup=return_in_menu_markup(),
        )


def get_film(message, bot):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {FilmStates.request}"
    )
    if (
        not bot.get_state(message.from_user.id, message.chat.id)
        == FilmStates.request.name
    ):
        return

    try:
        user_choice = int(message.text)
        if user_choice > 5 or user_choice < 1:
            raise ValueError

        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                films = data.get("films", None)

            film_data = films[user_choice - 1]

            kpoisk_api = KpoiskSettings()
            url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_data['kinopoiskId']}"
            headers = {
                "X-API-KEY": kpoisk_api.api.get_secret_value(),
                "Content-Type": "application/json",
            }

            response = requests.get(url, headers=headers)
            film_data = response.json()
            film_data["webUrl"] = film_data["webUrl"].replace(
                "kinopoisk.ru", "kinopoisk.vip"
            )

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["film"] = film_data

            stroke = (
                f"Название: {film_data['nameRu']}\n"
                f"Описание: {film_data['description']}\n"
                f"Страна: {film_data['countries'][0]['country']}\n"
                f"Год: {film_data['year']}\n"
                f"Рейтинг кинопоиска: {film_data['ratingKinopoisk']}\n\n"
                f"Смотрим?"
            )

            if film_data.get("posterUrl"):
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=film_data["posterUrl"],
                    caption=stroke,
                    reply_markup=under_film_markup(),
                )
            else:
                bot.send_message(
                    message.chat.id, stroke, reply_markup=under_film_markup()
                )

    except ValueError:
        bot.reply_to(
            message,
            "Некорректный ввод. Пожалуйста, введите номер фильма.",
            reply_markup=return_in_menu_markup(),
        )
        bot.register_next_step_handler(message, get_film, bot)


def give_url(bot, message, username):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {FilmStates.give_url}"
    )
    if not (
        bot.get_state(message.from_user.id, message.chat.id) == FilmStates.give_url.name
    ) or (
        bot.get_state(message.from_user.id, message.chat.id)
        == FilmStates.random_film.name
    ):
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        film = data.get("film", None)

    kpoisk_api = (
        KpoiskSettings()
    )  # иногда бывает так, что, например, при выборе рандомного фильма в полученном
    # json-ответе нет ключа 'webUrl', поэтому делаю еще один запрос по ID фильма, чтоб точно получить его url
    url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film['kinopoiskId']}"
    headers = {
        "X-API-KEY": kpoisk_api.api.get_secret_value(),
        "Content-Type": "application/json",
    }

    film_url = requests.get(url=url, headers=headers).json()["webUrl"]

    add_viewed_material(
        login=username, material_name=film["nameRu"], material_url=film_url
    )

    message_text = (
        f"Ссылка для просмотра: {film_url.replace('kinopoisk.ru', 'kinopoisk.vip')}\n"
        f"Приятного просмотра!\n\n"
        "<tg-spoiler>"
        "P.S. Не гарантирую, что ссылка будет рабочей т.к. не все фильмы есть на этом источнике.\n"
        f"Ссылка на кинопоиск: {film_url.replace('kinopoisk.vip', 'kinopoisk.ru')}"
        "</tg-spoiler>"
    )

    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=return_in_menu_markup(),
        parse_mode="HTML",
    )


def get_random_film(bot, message):
    print(
        f"Текущее состояние: {bot.get_state(message.from_user.id, message.chat.id)}. Ожидается: {FilmStates.random_film.name}"
    )
    if (
        not bot.get_state(message.from_user.id, message.chat.id)
        == FilmStates.random_film.name
    ):
        return

    kpoisk_api = KpoiskSettings()
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films/collections"
    headers = {
        "X-API-KEY": kpoisk_api.api.get_secret_value(),
        "Content-Type": "application/json",
    }

    films = []

    for i in range(12):
        params = {"type": "TOP_250_MOVIES", "page": i + 1}

        try:
            request = requests.get(url=url, headers=headers, params=params)
            request.raise_for_status()
            req_json = request.json()

        except requests.HTTPError as http_err:
            print(f"Произошла ошибка HTTP: {http_err}")
            bot.send_message(
                message.chat.id,
                "Произошла ошибка при получении фильма, попробуйте еще раз позже.",
                reply_markup=return_in_menu_markup(),
            )
            return
        except Exception as err:
            print(f"Произошла ошибка: {err}")
            bot.send_message(
                message.chat.id,
                "Произошла ошибка при получении фильма, попробуйте еще раз позже.",
                reply_markup=return_in_menu_markup(),
            )
            return

    films.extend(req_json.get("items", None))
    random_film = random.choice(films)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["film"] = random_film

    stroke = (
        f"Название: {random_film['nameRu']}\n"
        f"Описание: {random_film['description']}\n"
        f"Страна: {random_film['countries'][0]['country']}\n"
        f"Жанр: {random_film['genres'][0]['genre']}\n"
        f"Год: {random_film['year']}\n"
        f"Рейтинг кинопоиска: {random_film['ratingKinopoisk']}\n\n"
        f"Смотрим?"
    )

    if random_film.get("posterUrl"):
        bot.send_photo(
            chat_id=message.chat.id,
            photo=random_film["posterUrl"],
            caption=stroke,
            reply_markup=under_random_film(),
        )

    else:
        bot.send_message(message.chat.id, stroke, reply_markup=under_random_film())
