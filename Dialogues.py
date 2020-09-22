import AsyncQueue
import NumberKeyboard
import aiogram
import random


async def asc_question_dialogue(bot: aiogram.Bot, chat_id, queue: AsyncQueue.AsyncQueue, question, answers,
                                wrong_answer, correct_answer=None):
    markup_rpc = aiogram.types.ReplyKeyboardMarkup()
    markup_rpc.row(*answers)
    answer = None
    await bot.send_message(chat_id, question, reply_markup=markup_rpc)
    while True:
        # Получение нужных данных
        m = await queue.get_message()
        if not isinstance(m, aiogram.types.Message):
            await bot.send_message(chat_id, wrong_answer, reply_markup=markup_rpc)
            continue
        answer = m.text
        if answer not in answers:
            await bot.send_message(chat_id, wrong_answer, reply_markup=markup_rpc)
            continue
        break
    if correct_answer is not None:
        await bot.send_message(chat_id, correct_answer, reply_markup=aiogram.types.ReplyKeyboardRemove())
    return answer


async def number_dialogue(bot: aiogram.Bot, chat_id, queue: AsyncQueue.AsyncQueue):
    try:
        keyboard, context = NumberKeyboard.get_keyboard()
        input = await bot.send_message(chat_id, "Число: 0", reply_markup=keyboard)
        while True:
            m = await queue.get_message()
            if not isinstance(m, aiogram.types.CallbackQuery):
                await bot.send_message(chat_id, "Введите число с клавиатуры!", reply_markup=None)
                continue
            if NumberKeyboard.handle_input(m.data, context):
                await bot.edit_message_text(
                    chat_id=input.chat.id,
                    message_id=input.message_id,
                    text=f"Число: {context.value}",
                    reply_markup=keyboard)
            if context.completed:
                break
        await bot.send_message(chat_id, f"Вы ввели: {context.value}", reply_markup=None)
    except Exception as exc:
        await bot.send_message(chat_id, f"У меня что-то сломалось :(\n\n{exc}", reply_markup=None)


async def rock_paper_scissors_dialogue(bot: aiogram.Bot, chat_id, queue: AsyncQueue.AsyncQueue):
    try:
        items = ['камень', 'ножницы', 'бумага']
        answers = ['Да!', 'Нет.']
        markup_clear = aiogram.types.ReplyKeyboardRemove()
        await bot.send_message(chat_id,
                               "Играем в Камень-Ножницы-Бумага.\nЯ загадываю что-то одно и говорю, чем оно не является.\nПоехали!",
                               reply_markup=markup_clear)
        while True:
            choice = items[random.randint(0, 2)]
            others = [item for item in items if item != choice]
            randItem = others[random.randint(0, 1)]

            answer = await asc_question_dialogue(
                bot, chat_id, queue,
                f"Я загадал что-то, и это не {randItem}\nВаш выбор!",
                items, "Введите один из трёх предметов!")

            # получили ответ - анализируем!
            if choice == answer:
                await bot.send_message(chat_id, f"Вы загадали: {answer}\nЯ загадал тоже самое!\nУ нас ничья!",
                                       reply_markup=markup_clear)
            elif (choice == 'камень' and answer == 'ножницы') or \
                    (choice == 'ножницы' and answer == 'бумага') or \
                    (choice == 'бумага' and answer == 'камень'):
                await bot.send_message(chat_id, f"Вы загадали: {answer}\nЯ загадал: {choice}\nЯ победил!",
                                       reply_markup=markup_clear)
            elif (answer == 'камень' and choice == 'ножницы') or \
                    (answer == 'ножницы' and choice == 'бумага') or \
                    (answer == 'бумага' and choice == 'камень'):
                await bot.send_message(chat_id, f"Вы загадали: {answer}\nЯ загадал: {choice}\nВы победили!",
                                       reply_markup=markup_clear)

            answer = await asc_question_dialogue(
                bot, chat_id, queue,
                "Желаете сыграть ещё раз?",
                answers, "Эмм? Не понял...", "Отлично!")

            if answer == 'Да!':
                continue
            break
        await bot.send_message(chat_id, "Спасибо что плаваете поездами аэрофлота!", reply_markup=markup_clear)
    except Exception as exc:
        await bot.send_message(chat_id, f"У меня что-то сломалось :(\n\n{exc}", reply_markup=markup_clear)


async def test_dialogue(bot: aiogram.Bot, chat_id, queue: AsyncQueue.AsyncQueue):
    try:
        while True:
            answer_1 = await asc_question_dialogue(
                bot, chat_id, queue,
                f"Привет, хочешь поговорить? (͡ ° ͜ʖ ͡ °)",
                ['Да', 'Нет', 'Похуй'], "Выберите один из вариантов ответа!", "Угу...")

            if answer_1 == 'Да':
                answer_2 = await asc_question_dialogue(
                    bot, chat_id, queue,
                    f"Ты щас не поверишь, но у меня для тебя есть ДВА ПОДДИАЛОГА НА ВЫБОР!\n\n(￣ ー ￣)\nУгадай какие?)))",
                    ['Набор чиселок!', 'Игра в КНБ!'], "Выберите один из вариантов ответа :D", "Так-так-таааок!")
                if answer_2 == 'Набор чиселок!':
                    await number_dialogue(bot, chat_id, queue)
                elif answer_2 == 'Игра в КНБ!':
                    await rock_paper_scissors_dialogue(bot, chat_id, queue)
            elif answer_1 == 'Нет':
                url = "https://cdn.discordapp.com/attachments/640580712927461382/758034475375657058/unknown.png"
                await bot.send_photo(chat_id, url)
                await bot.send_message(chat_id, "Окей, диалог закончен :P")
                break
            elif answer_1 == 'Похуй':
                url = "https://cdn.discordapp.com/attachments/247382340735729664/758033008467902464/unknown.png"
                await bot.send_photo(chat_id, url)
                await bot.send_message(chat_id, "Ну ты и ебобо...")

    except Exception as exc:
        await bot.send_message(chat_id, f"У меня что-то сломалось :(\n\n{exc}", reply_markup=markup_clear)
