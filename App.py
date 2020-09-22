import logging
import requests
import asyncio
import AsyncQueue
import aiogram
import Config
import Dialogues


Config.Load()

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=Config.data['TELEGRAM']['TOKEN'])
dp = aiogram.Dispatcher(bot)


dialogues_container = {}


async def StartDialogue(chat_id, dialogue):
    global dialogues_container
    queue = AsyncQueue.Create()
    dialogues_container[chat_id] = queue
    await dialogue(bot, chat_id, queue)
    del dialogues_container[chat_id]


def DispatchMessage(chat_id, message):
    if chat_id in dialogues_container:
        # Если с данным перцем идёт диалог - передаём сообщение в диалог
        dialogues_container[chat_id].add_message(message)
        return True
    # Если нет - ну хуй с ним!
    return False


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: aiogram.types.Message):
    print(message.chat.id)
    await message.reply("""Привет! Я тестовый бот.

У меня есть такие команды:
/start - для приветствия
/number - чтобы ввести число
/rock_paper_scissors - чтобы сыграть в камень-ножницы-бумагу
/test_dialogue - тестовый диалог. Предыдущие две команды в него включены
На всё остальное мне пох)
""")


@dp.message_handler(commands=['number'])
async def number_dialogue(message: aiogram.types.Message):
    await StartDialogue(message.chat.id, Dialogues.number_dialogue)


@dp.message_handler(commands=['rock_paper_scissors'])
async def rock_paper_scissors_dialogue(message: aiogram.types.Message):
    await StartDialogue(message.chat.id, Dialogues.rock_paper_scissors_dialogue)


@dp.message_handler(commands=['test_dialogue'])
async def test_dialogue(message: aiogram.types.Message):
    await StartDialogue(message.chat.id, Dialogues.test_dialogue)


@dp.message_handler()
async def process_regular_message(message: aiogram.types.Message):
    # диалоги пока существуют только для приватной переписки (иначе просто придётся выдумывать ещё фильтрацию по user_id
    if message.chat.type == "private":
        if DispatchMessage(message.chat.id, message):
            return
    await bot.send_message(message.chat.id, "И чо?)")


@dp.callback_query_handler()
async def process_callback_message(callback_query: aiogram.types.CallbackQuery):
    message = callback_query.message
    if message.chat.type == "private":
        if DispatchMessage(message.chat.id, callback_query):
            await bot.answer_callback_query(callback_query.id)
            return
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(message.chat.id, "И чо?)")





def Send(chat_id, message):
    asyncio.run(bot.send_message(chat_id, message))


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
    # Send(820216855, f"Я начал работать!")
    # while loop:
    #     time.sleep(1)
    # print("Aha!")
    # Send(820216855, f"Я начал работать!")

    # response = requests.get("https://docs.google.com/spreadsheets/d/1cadXA41KEDUGvX5qJmwv80PgFj8tsxblzVXV-I1kcKE/edit?usp=sharing")
    # print()
    # print(response)
    # print()
    # print(response.content)
    # print()
    # print()
