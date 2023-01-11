from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards.reply import main_kb
from bot.keyboards.inline import create_cities_kb, create_goods_kb, create_pagination_kb
from bot.services.services import get_price, get_reviews, get_pages_amount, get_review_text, check_user, add_user

class PageState(StatesGroup):
    page: State = State()

async def start_command(message: Message, state: FSMContext):
    if not check_user(message.from_user.id):
        add_user(message.from_user.id, f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name)
    await state.finish()
    await message.answer_photo(photo='AgACAgIAAxkBAAMyY76B185GTePaszkSl29uLtjAuzMAAsvEMRuS3_hJmbCyr0LPR1UBAAMCAAN4AAMtBA', caption='<b>Приветствуем вас в нашем магазине!</b>', reply_markup=main_kb)
    '''AgACAgIAAxkBAAITZmOoEx_VXvr-el40-Tc1Whdi0Mx6AAJcwjEbYxlASfrEo_uWach1AQADAgADeAADLAQ'''

async def process_cities_button(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(text='<b>Выберите город: </b>', reply_markup=await create_cities_kb())

async def process_back_button(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='<b>Выберите город: </b>', reply_markup=await create_cities_kb())
    await callback.answer()

async def process_choice_good_button(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='<b>Выберите товар: </b>', reply_markup=await create_goods_kb(callback.data.split(':')[1]))
    await callback.answer()

async def process_show_price_good(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    name, price = get_price(callback.data.lstrip('good:'))
    await callback.message.edit_text(text=f"<b>{name}</b>\n<b>Цена: </b>\n\n{price}")
    await callback.answer()

async def process_connect_operator_button(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Выберите свой город: ', reply_markup=await create_cities_kb(connect=True))

async def process_review_button(message: Message, state: FSMContext):
    await state.finish()
    reviews = get_reviews()
    await PageState.page.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(reviews=reviews, page=1, pages_amount=get_pages_amount(len(reviews)))
    await message.answer(text=f"<b>Всего отзывов: {len(reviews)}</b>", reply_markup=await create_pagination_kb(reviews, 1, get_pages_amount(len(reviews))))

async def process_forward_button(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['page'] + 1 <= data['pages_amount']:
        await state.update_data(page=data['page']+1)
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=data['page'] + 1, pages_amount=data['pages_amount']))
    else:
        await state.update_data(page=1)
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=1, pages_amount=data['pages_amount']))
    await callback.answer()

async def process_backward_button(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['page'] - 1 > 0:
        await state.update_data(page=data['page']-1)
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=data['page'] - 1, pages_amount=data['pages_amount']))
    else:
        await state.update_data(page=data['pages_amount'])
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=data['pages_amount'], pages_amount=data['pages_amount']))
    await callback.answer()

async def process_review_check_button(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(text=get_review_text(data['reviews'][int(callback.data.lstrip('review:'))]))
    await callback.answer()

async def process_sale_button(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(text='- При покупке двух и более кладов в один день вы получаете скидку 20% на второй, 30% на третий и тд.\n\n- Приведи трех друзей в наш бот и получи бесплатный клад (подробности акции у оператора).\n\n- Каждая 10ая покупка с одного аккаунта в нашем магазине для вас будет бесплатной.')

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start', state='*')
    dp.register_message_handler(process_cities_button, text='Города', state='*')
    dp.register_callback_query_handler(process_choice_good_button, text_startswith='city', state='*')
    dp.register_callback_query_handler(process_back_button, text='back', state='*')
    dp.register_message_handler(process_connect_operator_button, text='Связаться с оператором', state='*')
    dp.register_callback_query_handler(process_show_price_good, text_startswith='good', state='*')
    dp.register_message_handler(process_review_button, text='Отзывы', state='*')
    dp.register_callback_query_handler(process_forward_button, text='forward', state=PageState.page)
    dp.register_callback_query_handler(process_backward_button, text='backward', state=PageState.page)
    dp.register_callback_query_handler(process_review_check_button, text_startswith='review', state='*')
    dp.register_message_handler(process_sale_button, text='Наши акции', state='*')
