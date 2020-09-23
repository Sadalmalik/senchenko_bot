import aiogram
import Config


def get_user(message: aiogram.types.Message):
    users = Config.data['TELEGRAM']['USERS']
    uid = str(message.from_user.id)
    if uid not in users:
        users[uid] = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
        Config.Save()
    return users[uid]


def get_admins():
    users = Config.data['TELEGRAM']['USERS']
    return [user for user in users if 'admin' in user and users['admin']]
