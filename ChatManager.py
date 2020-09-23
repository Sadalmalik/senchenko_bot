import Config
import aiogram


chats = Config.data['TELEGRAM']['CHATS']


def init_chat(chat_id):
    chat_id = str(chat_id)
    if chat_id not in chats:
        chats[chat_id] = {"id": chat_id, "messages": []}
        Config.Save()


def add_message(message: aiogram.types.Message):
    chat_id = str(message.chat.id)
    if chat_id not in chats:
        chats[chat_id] = {"id": chat_id, "messages": []}
    chats[chat_id]["messages"].append({
        "date": message.date.strftime("%Y.%m.%d %H:%M:%S"),
        "from": message.from_user.username,
        "text": message.text
    })
    if Config.data['TELEGRAM']['CHATS_LIMIT']<=len(chats[chat_id]["messages"]):
        chats[chat_id]["messages"].pop(0)
    Config.Save()


def get_chat(chat_id):
    chat_id = str(chat_id)
    init_chat(chat_id)
    return chats[chat_id]


def get_messages(chat_id, count, username=None):
    chat_id = str(chat_id)
    if chat_id not in chats:
        return []
    messages = chats[chat_id]["messages"]
    if count > len(messages):
        return messages
    if username:
        messages = [mes for mes in messages if mes['from'] == username]
    return messages[-count:]
