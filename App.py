# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import telegram
import Config
import json
import time
from telegram.ext import Updater
from telegram.ext import Filters, MessageHandler, CommandHandler
import random
import GoogleForm

Config.Load()

loop: bool = True

def main():
    global loop
    bot = telegram.Bot(token=Config.data['TELEGRAM']['TOKEN'])
    bot.send_message(chat_id=820216855, text="Однако дратути!")

    def HandleCommand(bot, update):
        global loop
        result = f"Input command:\n{json.dumps(bot)}\n{json.dumps(update)}"
        print(result)
        bot.send_message(chat_id=820216855, text=result)
        if update.message.lower() == "/stop":
            loop = False

    def Stop(update, context):
        print("AfFAfaaf")
        global loop
        try:
            result = f"Input command:\n\n{update}\n\n\n{context}"
            print(result)
            bot.send_message(chat_id=820216855, text=result)
            if update.message.text == "/stop":
                loop = False
        except Exception as exc:
            print(f"Error: {exc}")

    def HandleMessage(update, context):
        try:
            result = f"Input command:\n\n{update}\n\n\n{context}"
            print(result)
            bot.send_message(chat_id=820216855, text=result)
        except Exception as exc:
            print(f"Error: {exc}")

    updater = Updater(token=Config.data['TELEGRAM']['TOKEN'], use_context=True)
    # updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stop', Stop), group=0)
    # updater.dispatcher.add_handler(MessageHandler(Filters.command, HandleCommand), group=1)
    updater.dispatcher.add_handler(MessageHandler(None, HandleMessage), group=1)
    updater.start_polling()

    while loop:
        print("Wait")
        time.sleep(10)
    print("Loop complete")


# entry.866341572: Глб
# entry.1846785254: Опа-па
# fvv: 1
# draftResponse: [null,null,"-4418110148297938397"]
# pageHistory: 0
# fbzx: -4418110148297938397
def Store(name, content):
    jokeForm = "1FAIpQLSe_NtxJ9lxQ9ewMtZ1hRt8XyrbxamxNZNi5E1MvIsijCnjLTQ"
    GoogleForm.Send(jokeForm, {
        "entry.866341572": name,
        "entry.1846785254": content,
        "fvv": 1
    })


if __name__ == '__main__':
    # main()
    Store("BOT", "TEST JOKE 1")
    Store("BOT", "TEST JOKE 2")
    Store("BOT", "TEST JOKE 3")
