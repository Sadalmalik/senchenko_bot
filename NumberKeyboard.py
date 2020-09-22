import aiogram


class Context:
    def __init__(self):
        self.value = "0"
        self.completed = False


def get_keyboard():
    inline = aiogram.types.InlineKeyboardMarkup()
    inline.row(
        aiogram.types.InlineKeyboardButton('1', callback_data='1'),
        aiogram.types.InlineKeyboardButton('2', callback_data='2'),
        aiogram.types.InlineKeyboardButton('3', callback_data='3'))
    inline.row(
        aiogram.types.InlineKeyboardButton('4', callback_data='4'),
        aiogram.types.InlineKeyboardButton('5', callback_data='5'),
        aiogram.types.InlineKeyboardButton('6', callback_data='6'))
    inline.row(
        aiogram.types.InlineKeyboardButton('7', callback_data='7'),
        aiogram.types.InlineKeyboardButton('8', callback_data='8'),
        aiogram.types.InlineKeyboardButton('9', callback_data='9'))
    inline.row(
        aiogram.types.InlineKeyboardButton('<<', callback_data='<<'),
        aiogram.types.InlineKeyboardButton('0', callback_data='0'),
        aiogram.types.InlineKeyboardButton('OK', callback_data='OK'))
    return inline, Context()


def handle_input(value, context: Context):
    if value in "0123456789":
        context.value = context.value.lstrip('0') + value
        return True
    elif value == '<<':
        context.value = context.value[:len(context.value)-1]
        if len(context.value) == 0:
            context.value = '0'
        return True
    elif value == 'OK':
        context.completed = True
    return False
