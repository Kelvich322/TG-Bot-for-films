from telebot import types

# def simple_markup(): #пример базовой инлайн-кнопки, которая ничего не делает
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton('Test', callback_data='func_name'))
#     return markup


def return_in_menu_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Вернуться в главное меню", callback_data="menu")
    )
    return markup


def yes_or_again_markup():
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data="request_film")
    btn_again = types.InlineKeyboardButton("Выбрать заново", callback_data="again")
    btn_menu = types.InlineKeyboardButton(
        "Вернуться в главное меню", callback_data="menu"
    )
    markup.row(btn_yes, btn_again)
    markup.add(btn_menu)
    return markup


def again_markup():
    markup = types.InlineKeyboardMarkup()
    btn_again = types.InlineKeyboardButton("Выбрать заново", callback_data="again")
    btn_menu = types.InlineKeyboardButton(
        "Вернуться в главное меню", callback_data="menu"
    )
    markup.row(btn_again, btn_menu)
    return markup


def under_film_markup():
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data="give_url")
    btn_no = types.InlineKeyboardButton(
        "Выбрать другой фильм", callback_data="another_film"
    )
    btn_again = types.InlineKeyboardButton(
        "Выбрать жанр и год заново", callback_data="again"
    )
    btn_menu = types.InlineKeyboardButton(
        "Вернуться в главное меню", callback_data="menu"
    )
    markup.row(btn_yes, btn_no)
    markup.add(btn_again)
    markup.add(btn_menu)
    return markup


def under_random_film():
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data="give_url")
    btn_no = types.InlineKeyboardButton(
        "Получить другой фильм", callback_data="random_again"
    )
    btn_menu = types.InlineKeyboardButton(
        "Вернуться в главное меню", callback_data="menu"
    )
    markup.row(btn_yes, btn_no)
    markup.add(btn_menu)
    return markup
