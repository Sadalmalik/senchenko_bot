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
import traceback

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=Config.data['TELEGRAM']['TOKEN'])
dp = aiogram.Dispatcher(bot)


async def CheckUserForbidden(user, message: aiogram.types.Message, silence=False):
    if message.chat.type == "group":
        if "forbidden" in user and user["forbidden"]:
            if "forbidden-text" in user:
                if not silence:
                    await message.reply(
                        f'Извините, я не могу выполнить вашу команду в этом чате.\nПричина:\n\n{user["forbidden-text"]}')
            return True
    return False


async def NotificateAdmins(exc):
    admins = ConfigFunctions.get_admins()
    for admin in admins:
        await bot.send_message(admin['id'], Templates.exception_admin.format(exception=exc))


@dp.message_handler(commands=['start'])
async def send_welcome(message: aiogram.types.Message):
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    user_session = ConfigFunctions.get_user(message)
    chat_session = ChatManager.get_chat(chat_id)
    silence = chat_session['silence']
    if await CheckUserForbidden(user_session, message, silence):
        return
    try:
        if message.chat.type == 'private':
            await bot.send_message(chat_id, Templates.private_intro)
        elif message.chat.type == "group":
            ChatManager.init_chat(message.chat.id)
            await bot.send_message(chat_id, Templates.public_intro.format(
                message_default=Config.data['TELEGRAM']['CHATS_DEFAULT'],
                message_max=Config.data['TELEGRAM']['CHATS_LIMIT']
            ))
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        await NotificateAdmins(exc)


@dp.message_handler(commands=['talk'])
async def main_dialogue(message: aiogram.types.Message):
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    try:
        if message.chat.type == "private":
            await DialogueManager.start(bot, message.chat.id, Dialogues.main_dialogue)
        elif message.chat.type == "group":
            user_session = ConfigFunctions.get_user(message)
            chat_session = ChatManager.get_chat(chat_id)
            silence = chat_session['silence']
            if await CheckUserForbidden(user_session, message, silence):
                return
            if not silence:
                await bot.send_message(message.chat.id, "Эта команда доступна только в личной переписке!")
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        await NotificateAdmins(exc)



@dp.message_handler(commands=['mute'])
async def set_silence(message: aiogram.types.Message):
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    try:
        if message.chat.type == "private":
            await bot.send_message(message.chat.id, "Эта команда доступна только чате!")
        elif message.chat.type == "group":
            user_session = ConfigFunctions.get_user(message)
            chat_session = ChatManager.get_chat(chat_id)
            silence = chat_session['silence']
            if await CheckUserForbidden(user_session, message, silence):
                return
            flag = False
            arguments = message.text.split(' ')[1:]
            if len(arguments) > 0:
                flag = arguments[0].lower() == 'on'
            chat_session['silence'] = flag
            Config.Save()
            await bot.send_message(message.chat.id, "Режим молчания включен." if flag else "Режим молчания выключен.")
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        await NotificateAdmins(exc)


@dp.message_handler(commands=['last', 'l'])
async def save_last(message: aiogram.types.Message):
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    user_session = ConfigFunctions.get_user(message)
    chat_session = ChatManager.get_chat(chat_id)
    silence = chat_session['silence']
    if await CheckUserForbidden(user_session, message, silence):
        return
    try:
        if message.chat.type == "private":
            if not silence:
                await bot.send_message(message.chat.id, Templates.wrong_chat_joke)
        elif message.chat.type == "group":
            arguments = message.text.split(' ')[1:]
            count = Config.data['TELEGRAM']['CHATS_DEFAULT']
            if len(arguments) > 0:
                count = int(arguments[0])
            messages = ChatManager.get_messages(message.chat.id, count)
            if len(messages) > 0:
                is_serega = len([mes for mes in messages if mes['from'] == "captainkazah"]) > 0
                text = "\n\n".join([f"{mes['date']} {mes['from']}:\n{mes['text']}" for mes in messages])
                text = f"Chat: {message.chat.title}\n\n{text}"
                GoogleForm.StoreJoke(message.from_user.username, text, is_serega)
                if not silence:
                    await bot.send_message(message.chat.id, Templates.save_tamplate_multy.format(count=len(messages)))
            else:
                if not silence:
                    await bot.send_message(message.chat.id, Templates.save_fail_tamplate)
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        if not silence:
            await bot.send_message(chat_id, Templates.exception.format(exception=exc))
        await NotificateAdmins(exc)


@dp.message_handler(commands=['joke', 'j'])
async def save_joke(message: aiogram.types.Message):
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    chat_id = message.chat.id
    user_session = ConfigFunctions.get_user(message)
    chat_session = ChatManager.get_chat(chat_id)
    silence = chat_session['silence']
    if await CheckUserForbidden(user_session, message, silence):
        return
    try:
        if message.chat.type == "private":
            if not silence:
                await bot.send_message(message.chat.id, Templates.wrong_chat_joke)
        elif message.chat.type == "group":
            arguments = message.text.split(' ')[1:]
            name = "captainkazah"
            count = Config.data['TELEGRAM']['CHATS_DEFAULT']
            if len(arguments) > 0:
                name = arguments[0].strip().strip('@')
            if len(arguments) > 1:
                count = int(arguments[1].strip())
            messages = ChatManager.get_messages(message.chat.id, count, name)
            if len(messages) > 0:
                is_serega = len([mes for mes in messages if mes['from'] == "captainkazah"]) > 0
                text = "\n\n".join([f"{mes['date']} {mes['from']}:\n{mes['text']}" for mes in messages])
                text = f"Chat: {message.chat.title}\n\n{text}"
                GoogleForm.StoreJoke(message.from_user.username, text, is_serega)
                if not silence:
                    await bot.send_message(message.chat.id, Templates.save_tamplate_multy.format(count=len(messages)))
            else:
                if not silence:
                    await bot.send_message(message.chat.id, Templates.save_fail_tamplate)
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        if not silence:
            await bot.send_message(chat_id, Templates.exception.format(exception=exc))
        await NotificateAdmins(exc)



@dp.message_handler()
async def process_regular_message(message: aiogram.types.Message):
    logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
    try:
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
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        await NotificateAdmins(exc)


@dp.callback_query_handler()
async def process_callback_message(callback_query: aiogram.types.CallbackQuery):
    try:
        message = callback_query.message
        logging.info(f"Handle message <{message.message_id}> from @{message.from_user.username}")
        if message.chat.type == "private":
            if DialogueManager.dispatch_message(message.chat.id, callback_query):
                await bot.answer_callback_query(callback_query.id)
                return
        await bot.answer_callback_query(callback_query.id)
    except Exception as exc:
        logging.info(f"Exception: {exc}")
        traceback.print_exc()
        await NotificateAdmins(exc)


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
