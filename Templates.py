

private_intro = """Привет! Я бот)
Я буду сохранять все ваши текстовые сообщения и пересланные текстовые сообщения в специальную гугл таблицу для шуток.
Все сохранённые шутейки можно найти в гугл таблице:
https://docs.google.com/spreadsheets/d/1LPNBZIMGUUyyuuUU4MSS9BESMuECQshzs6hrtMOwJuU/edit?usp=sharing

Так же у меня есть такие команды:
/start - для этого приветствия
/talk - если вам скучно - то мы можем пообщаться :)
"""

public_intro = """Всем привет!
Я бот для сбора шуток!

Если тут происходит что-то смешное - пишите /joke или /j и я сохраню последние {message_default} сообщений.
Вы можете указать другое число сообщений: /j 7 - и я сохраню 7 сообщений.
Но не более {message_max}.
Так же вы можете присылать их мне в личку.

Все сохранённые шутейки можно найти в гугл таблице:
https://docs.google.com/spreadsheets/d/1LPNBZIMGUUyyuuUU4MSS9BESMuECQshzs6hrtMOwJuU/edit?usp=sharing
"""

wrong_chat_joke = """Команды /joke и /j доступны только в публичном чате."""

exception = """Во время моей работы случилась ошибка :(

Сообщите моему создателю:
{exception}
"""

save_tamplate = """Сохранил:
'{text}'

Все сохранённые шутейки можно найти в гугл таблице:
https://docs.google.com/spreadsheets/d/1LPNBZIMGUUyyuuUU4MSS9BESMuECQshzs6hrtMOwJuU/edit?usp=sharing
"""

save_tamplate_multy = """Сохранил сообщений: {count}

Все сохранённые шутейки можно найти в гугл таблице:
https://docs.google.com/spreadsheets/d/1LPNBZIMGUUyyuuUU4MSS9BESMuECQshzs6hrtMOwJuU/edit?usp=sharing
"""

save_fail_tamplate = """Мне не удалось сохранить сообщения...

У меня дырявая память и я не умею читать :(
Пожалуйста не ругайте меня :(
"""


main_dialogue_intro = """О! Ну давай общаться (͡ ° ͜ʖ ͡ °)

Я могу:
- дать панельку для ввода цифр
- поиграть с тобой в камень-ножницы-бумага
- поиграть с тобой в слова
"""

main_dialogue_continue = """Чем ещё займёмся?

Я могу:
- дать панельку для ввода цифр
- поиграть с тобой в камень-ножницы-бумага
- поиграть с тобой в слова
"""
