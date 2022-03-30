from aiogram import types

def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    male = types.KeyboardButton("мужская")
    female = types.KeyboardButton("женская")
    keyboard.add(male)
    keyboard.add(female)

    return keyboard