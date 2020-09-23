import aiogram
import Config


def check_user(message: aiogram.types.Message):
    users = Config.data['TELEGRAM']['USERS']
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
        Config.Save()
