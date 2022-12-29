from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
main_kb.add(*[
    KeyboardButton(text='Связаться с оператором'),
    KeyboardButton(text='Наши акции'),
    KeyboardButton(text='Города'),
    KeyboardButton(text='Отзывы')
])
