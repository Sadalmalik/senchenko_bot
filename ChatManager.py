import Config
import aiogram


chats = Config.data['TELEGRAM']['CHATS']


def init_chat(chat_id):
    if chat_id not in chats:
        chats[chat_id] = {"id": chat_id, "messages": []}
        Config.Save()


def add_message(message: aiogram.types.Message):
    chat_id = message.chat.id
    if chat_id not in chats:
        chats[chat_id] = {"id": chat_id, "messages": []}
    chats[chat_id]["messages"].append({
        "date": message.date,
        "from": message.from_user.username,
        "text": message.text
    })
    if Config.data['TELEGRAM']['CHATS_LIMIT']<=len(chats[chat_id]["messages"]):
        chats[chat_id]["messages"].pop(0)
    Config.Save()


def get_messages(chat_id, count):
    if chat_id not in chats:
        return []
    if count > len(chats[chat_id]["messages"]):
        return chats[chat_id]["messages"]
    return chats[chat_id]["messages"][-count:]
