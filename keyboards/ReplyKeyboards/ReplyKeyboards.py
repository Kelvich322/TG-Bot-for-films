from telebot import types


def keyboard_to_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать фильм")
    btn2 = types.KeyboardButton("Выбрать случайный фильм")
    btn3 = types.KeyboardButton("История просмотра")

    markup.row(btn1, btn2)
    markup.add(btn3)
    return markup


def remove_markup():
    markup = types.ReplyKeyboardRemove(selective=True)
    return markup
