import AsyncQueue
import aiogram


dialogues_container = {}


async def start(bot: aiogram.Bot, chat_id, dialogue):
    global dialogues_container
    queue = AsyncQueue.Create()
    dialogues_container[chat_id] = queue
    await dialogue(bot, chat_id, queue)
    del dialogues_container[chat_id]


def dispatch_message(chat_id, message):
    if chat_id in dialogues_container:
        # Если с данным перцем идёт диалог - передаём сообщение в диалог
        dialogues_container[chat_id].add_message(message)
        return True
    # Если нет - ну хуй с ним!
    return False