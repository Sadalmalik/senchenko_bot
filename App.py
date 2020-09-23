import Config
import ConfigFunctions

Config.Load()

import logging
# import requests
# import asyncio
import aiogram
import Dialogues
import DialogueManager
import Templates
import ChatManager
import GoogleForm

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=Config.data['TELEGRAM']['TOKEN'])
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: aiogram.types.Message):
    ConfigFunctions.check_user(message)
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    if message.chat.type == 'private':
        await bot.send_message(chat_id, Templates.private_intro)
    else:
        ChatManager.init_chat(message.chat.id)
        await bot.send_message(chat_id, Templates.public_intro.format(
            message_default=Config.data['TELEGRAM']['CHATS_DEFAULT'],
            message_max=Config.data['TELEGRAM']['CHATS_LIMIT']
        ))


@dp.message_handler(commands=['talk'])
async def number_dialogue(message: aiogram.types.Message):
    ConfigFunctions.check_user(message)
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    await DialogueManager.start(bot, message.chat.id, Dialogues.main_dialogue)


@dp.message_handler(commands=['joke', 'j'])
async def test_dialogue(message: aiogram.types.Message):
    ConfigFunctions.check_user(message)
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    try:
        arguments = message.text.split(' ')[1:]
        count = Config.data['TELEGRAM']['CHATS_DEFAULT']
        if len(arguments) > 0:
            count = int(arguments[0])
        messages = ChatManager.get_messages(chat_id, count)
        if len(messages)>0:
            is_serega = len([mes for mes in messages if mes['from'] == "captainkazah"]) > 0
            text = "\n\n".join([f"{mes['date']} {mes['from']}:\n{mes['text']}" for mes in messages])
            GoogleForm.StoreJoke(message.from_user.username, text, is_serega)
            await bot.send_message(message.chat.id, Templates.save_tamplate_multy.format(count=len(messages)))
        else:
            await bot.send_message(message.chat.id, Templates.save_fail_tamplate)
    except Exception as exc:
        await bot.send_message(chat_id, Templates.exception.format(exception=exc))


@dp.message_handler()
async def process_regular_message(message: aiogram.types.Message):
    ConfigFunctions.check_user(message)
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    # диалоги пока существуют только для приватной переписки (иначе просто придётся выдумывать ещё фильтрацию по user_id
    if message.chat.type == "private":
        if DialogueManager.dispatch_message(message.chat.id, message):
            return
        is_serega = False
        is_serega = is_serega or (message.forward_from and message.forward_from.username == "captainkazah")
        is_serega = is_serega or (message.from_user.username == "captainkazah")
        GoogleForm.StoreJoke(message.from_user.username, message.text, is_serega)
        await bot.send_message(message.chat.id, Templates.save_tamplate.format(text=message.text))
    else:
        ChatManager.add_message(message)


@dp.callback_query_handler()
async def process_callback_message(callback_query: aiogram.types.CallbackQuery):
    message = callback_query.message
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    if message.chat.type == "private":
        if DialogueManager.dispatch_message(message.chat.id, callback_query):
            await bot.answer_callback_query(callback_query.id)
            return
    await bot.answer_callback_query(callback_query.id)


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
