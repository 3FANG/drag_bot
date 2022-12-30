from collections import namedtuple

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.services.services import get_cities, get_goods, get_city_operator_link

cancel_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel')]])

async def create_cities_kb(editing=False, delete=False, separately=False, connect=False):
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    if editing:
        for city in get_cities():
            kb.add(InlineKeyboardButton(text=f"✏️ {city}", callback_data=f"ed_city:{city}"))
        kb.add(InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel'))
    elif delete:
        if separately:
            for city in get_cities():
                kb.add(InlineKeyboardButton(text=f"📍 {city}", callback_data=f"in_city:{city}"))
        else:
            for city in get_cities():
                kb.add(InlineKeyboardButton(text=f"❌ {city}", callback_data=f"del_city:{city}"))
        kb.add(InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel'))
    elif connect:
        for city, link in get_city_operator_link():
            kb.add(InlineKeyboardButton(text=f"{city}", url=link))
    else:
        for city in get_cities():
            kb.add(InlineKeyboardButton(text=f"{city}", callback_data=f"city:{city}"))
    return kb

async def create_goods_kb(city: str=None, editing=False, delete=False, separately=False):
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    if editing:
        for id, good, price in get_goods(city):
            kb.add(InlineKeyboardButton(text=f"✏️ {good}", callback_data=f"ed_good:{id}"))
        kb.add(InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel'))
    elif delete:
        if separately:
            for id, good, price in get_goods(city):
                # print(len(f"put_away_good:{good}".encode()), f"put_away_good:{id}")
                kb.add(InlineKeyboardButton(text=f"❌ {good}", callback_data=f"put_away_good:{id}"))
        else:
            for id, good, price in get_goods(city):
                kb.add(InlineKeyboardButton(text=f"❌ {good}", callback_data=f"del_good:{id}"))
        kb.add(InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel'))
    else:
        for id, good, price in get_goods(city):
            kb.add(InlineKeyboardButton(text=f"{good}", callback_data=f"good:{id}"))
        kb.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return kb

async def create_admin_panel_kb():
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    kb.add(*[
        InlineKeyboardButton(text='🟣 Добавить город', callback_data='add_city'),
        InlineKeyboardButton(text='🟣 Добавить товар', callback_data='add_good'),
        InlineKeyboardButton(text='🟣 Добавить отзыв', callback_data='add_review'),
        InlineKeyboardButton(text='🟣 Добавить товар в город', callback_data='add_good_in_city')
    ])
    kb.add(*[
        InlineKeyboardButton(text='🔴 Удалить город', callback_data='delete_city'),
        InlineKeyboardButton(text='🔴 Удалить товар', callback_data='delete_good'),
        InlineKeyboardButton(text='🔴 Удалить отзыв', callback_data='delete_review'),
        InlineKeyboardButton(text='🔴 Удалить товар из города', callback_data='delete_good_in_city'),
    ])
    return kb

async def create_pagination_kb(reviews: list[namedtuple], page: int, pages_amount: int, delete=False):
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)
    for index, review in enumerate(reviews[(page-1)*10:page*10]):
        if not delete:
            kb.add(InlineKeyboardButton(text=f"{review.rating}/10 | {review.date.replace('-', '.')}", callback_data=f"review:{index+(10*(page-1))}"))
        else:
            kb.add(InlineKeyboardButton(text=f"❌ {review.rating}/10 | {review.date.replace('-', '.')}", callback_data=f"del_review:{index+(10*(page-1))}"))
    kb.add(*[
        InlineKeyboardButton(text='<<', callback_data='backward'),
        InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data='none'),
        InlineKeyboardButton(text='>>', callback_data='forward')
    ])
    if delete:
        kb.add(InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel'))
    return kb
