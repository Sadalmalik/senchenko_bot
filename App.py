"""
This is a echo bot.
It echoes any incoming text messages.
"""

import asyncio
import logging
import requests
import Config
import time

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

Config.Load()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Config.data['TELEGRAM']['TOKEN'])
dp = Dispatcher(bot)

bot_info = """Привет!
Я пока ещё тестовый бот.
Что бы меня выключить - напишите /stop
"""
loop = True


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    print(message.chat.id)
    await message.reply(bot_info)


@dp.message_handler(commands=['stop'])
async def send_welcome(message: types.Message):
    global loop
    loop = False
    await message.reply("Я завершаю свою работу!")


#
#
# @dp.message_handler(state="*")
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#     await message.answer(f"You send: {message.text}")


def get_reply_keyboard():
    reply = ReplyKeyboardMarkup(resize_keyboard=True)
    reply.row("Да", "Нет", "Отмена")
    return reply


def get_inline_keyboard():
    inline = InlineKeyboardMarkup()
    inline.row(
        InlineKeyboardButton('Да', callback_data='Yes'),
        InlineKeyboardButton('Нет', callback_data='No'),
        InlineKeyboardButton('Пропустить', callback_data='Skip')
    )
    return inline


@dp.message_handler(commands=['go'], state="*")
async def start_answering(message: types.Message):
    await message.answer("Выберите блюдо:", reply_markup=get_reply_keyboard())


@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"Ваш ответ: '{callback_query.data}'")
    await bot.answer_callback_query(callback_query.id)


def Send(chat_id, message):
    asyncio.run(bot.send_message(chat_id, message))


if __name__ == '__main__':
    loop = True
    Send(820216855, f"Я начал работать!")
    asyncio.run(dp.start_polling())
    print("Aha!")
    while loop:
        time.sleep(1)
    print("Aha!")
    dp.stop_polling()
    Send(820216855, f"Я закончил работать!")

    # response = requests.get("https://docs.google.com/spreadsheets/d/1cadXA41KEDUGvX5qJmwv80PgFj8tsxblzVXV-I1kcKE/edit?usp=sharing")
    # print()
    # print(response)
    # print()
    # print(response.content)
    # print()
    # print()
