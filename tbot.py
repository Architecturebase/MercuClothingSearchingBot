import aiogram
from time import time
from yolo.utils.utils import *
from predictors.YOLOv3 import YOLOv3Predictor
from PIL import Image

from new_image_demo import detectioner
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from WB_parser import parsing_male, parsing_female, links_returner, parsing
from config import TOKEN
from keyboard import get_keyboard

from Color_Detection import get_image, get_colors, hex2name, color_names, RGB2HEX, color_translate

#load_dotenv()
os.getenv("TOKEN")
#инициализация бота
bot = Bot(token = TOKEN)
#dp - это диспетчер, в которого мы передаём бота
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    print(user_name)

    # await message.reply(f'Привет, {user_name}! Твой user id = {user_id}!')
    await message.reply(f'Привет! Загрузи фото и получи ссылки на интернет-магазины!')
#await - аналог return для асинхронных функций в python

# @dp.message_handler(content_types = ['text'])
# async def echo(message: types.Message):
#     await message.reply(message.txt)

# @dp.message_handler(content_types=['photo'])
# async def echo(message: types.Message):
#     user_name = message.from_user.first_name
#     await message.reply(f'Извини, {user_name}, я не работаю с фото!')

@dp.message_handler(content_types=['photo'])
async def echo(message: types.Message):
    chat_id = message.chat.id
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    message_id = message.message_id
    #тут он должен будет отправлять фото и ссылки на интернет-магазины
    #для этого он выделит признаки и спарсит ссылки
    photo_path = './tg_img_loaded/photo_%s_%s.jpg' %(user_id, message_id)
    await message.photo[-1].download(photo_path)
    # img = cv2.imread(photo_path)
    detections = detectioner(photo_path)
    if len(detections) == 0:
        await message.reply('Ничего не нашел... Отправь другое фото')
    else:
        # await message.reply(f'{detections}')
        cropped_path = './cropped/cropped_photo_%s_%s.jpg' %(user_id, message_id)
        cropped_image = get_image(cropped_path)
        colors = get_colors(cropped_image, 3, False)
        # hexed_colors = hex2name(colors)
        colors_list_named = color_names(colors)
        colors_ru = color_translate(colors_list_named)

        await message.reply('Одежда для какого пола тебя интересует?', reply_markup=get_keyboard())

        @dp.message_handler(lambda message: message.text and 'мужская' in message.text.lower())
        async def text_handler(message: types.Message):
            chat_id = message.chat.id
            await bot.send_chat_action(chat_id, 'typing')
            links_list_male = await parsing_male(detections, colors_ru)
            num_links = 2
            print(links_list_male)
            for item in links_list_male:
                result_link = links_returner(item)
                print(result_link)
                await bot.send_chat_action(chat_id, 'typing')

                if result_link:
                    await message.reply(f'{result_link}')


        @dp.message_handler(lambda message: message.text and 'женская' in message.text.lower())
        async def text_handler(message: types.Message):
            chat_id = message.chat.id
            await bot.send_chat_action(chat_id, 'typing')
            links_list_female = await parsing_female(detections, colors_ru)
            num_links = 2
            print(links_list_female)
            for item in links_list_female:
                result_link = links_returner(item)
                print(result_link)
                await bot.send_chat_action(chat_id, 'typing')

                if result_link:
                    await message.reply(f'{result_link}')



#команда запуска бота
if __name__ == '__main__': # всегда True
    executor.start_polling(dp)
