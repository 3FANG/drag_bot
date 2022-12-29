from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.config.config import load_config
from bot.keyboards.inline import create_admin_panel_kb, create_cities_kb, create_goods_kb, cancel_kb, create_pagination_kb
from bot.services.services import add_city, add_good, add_good_in_city, del_city, del_good, del_review, del_good_from_city, check_date, check_rating, add_review, get_pages_amount, get_reviews

CFG = load_config()

class AdminState(StatesGroup):
    add_city: State = State()
    add_operator: State = State()
    add_good: State = State()
    add_price: State = State()
    add_good_in_city: State = State()
    del_good_in_city: State = State()

    add_date: State = State()
    add_rating: State = State()
    add_customer: State = State()
    add_review: State = State()

    page: State = State()

async def admin_panel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(text='<i><b>Админ панель</b></i>', reply_markup=await create_admin_panel_kb())

async def process_cancel_button(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='<i><b>Админ панель</b></i>', reply_markup=await create_admin_panel_kb())

async def process_add_city_button(callback: CallbackQuery):
    await callback.message.edit_text(text='📝 Введите город...', reply_markup=cancel_kb)
    await AdminState.add_city.set()
    await callback.answer()

async def process_write_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await AdminState.add_operator.set()
    await message.answer('📝 Введите ссылку на оператора(https://t.me/...)...', reply_markup=cancel_kb)

async def process_add_operator(message: Message, state: FSMContext):
    if not message.text.startswith('https://t.me/'):
        await message.answer('❕ <i>Некорректная ссылка</i>')
        return
    data = await state.get_data()
    add_city(data['city'], message.text)
    await message.answer('✔️ Город успешно добавлен')
    await state.finish()

async def process_add_good_button(callback: CallbackQuery):
    await callback.message.edit_text(text='📝 Введите название товара...', reply_markup=cancel_kb)
    await AdminState.add_good.set()
    await callback.answer()

async def process_write_good(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='📝 Введите цену...')
    await AdminState.add_price.set()

async def process_write_price(message: Message, state: FSMContext):
    data = await state.get_data()
    add_good(data['name'], message.html_text)
    await message.answer(text='✔️ Товар успешно добавлен')
    await state.finish()

async def process_add_good_in_city_button(callback: CallbackQuery):
    await AdminState.add_good_in_city.set()
    await callback.message.edit_text(text='🟡 <b>Выберите город, в который хотите добавить товар: </b>', reply_markup=await create_cities_kb(editing=True))
    await callback.answer()

async def process_add_good_in_city(callback: CallbackQuery, state: FSMContext):
    await state.update_data(city=callback.data.lstrip('ed_city:'))
    await callback.message.edit_text(text='🟡 <b>Выберите товар, который хотите добавить: </b>', reply_markup=await create_goods_kb(editing=True))
    await callback.answer()

async def process_update_stock_add(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    add_good_in_city(data['city'], callback.data.lstrip('ed_good:'))
    await callback.message.edit_text(text=f"✔️ <b>Наличие товара в городе {data['city']} обновлено</b>")
    await state.finish()
    await callback.answer()

async def delete_city_button(callback: CallbackQuery):
    await callback.message.edit_text(text='🔴 <b>Выберите город, который хотите удалить: </b>', reply_markup=await create_cities_kb(delete=True))
    await callback.answer()

async def process_delete_city(callback: CallbackQuery):
    del_city(callback.data.lstrip('del_city:'))
    await callback.message.edit_text(text='✔️ Город успешно удалён')
    await callback.answer()

async def delete_good_button(callback: CallbackQuery):
    await callback.message.edit_text(text='🔴 <b>Выберите товар, который хотите удалить: </b>', reply_markup=await create_goods_kb(delete=True))
    await callback.answer()

async def process_delete_good(callback: CallbackQuery):
    del_good(callback.data.lstrip('del_good:'))
    await callback.message.edit_text(text='✔️ Товар успешно удалён')
    await callback.answer()

async def process_del_good_in_city_button(callback: CallbackQuery):
    await AdminState.del_good_in_city.set()
    await callback.message.edit_text(text='🟠 <b>Выберите город, в котором хотите удалить товар: </b>', reply_markup=await create_cities_kb(delete=True, separately=True))
    await callback.answer()

async def process_del_good_in_city(callback: CallbackQuery, state: FSMContext):
    await state.update_data(city=callback.data.lstrip('in_city:'))
    await callback.message.edit_text(text='🔴 <b>Выберите товар, который хотите удалить: </b>', reply_markup=await create_goods_kb(city=callback.data.lstrip('in_city:'), delete=True, separately=True))
    await callback.answer()

async def procecc_update_stock_del(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del_good_from_city(data['city'], callback.data.lstrip('put_away_good:'))
    await callback.message.edit_text(text='✔️ Товар успешно удалён из города')
    await state.finish()
    await callback.answer()

async def process_add_review_button(callback: CallbackQuery):
    await AdminState.add_date.set()
    await callback.message.answer('📝 Введите дату отзыва в формате ДД-ММ-ГГГГ(например, 01-01-1970)...')
    await callback.answer()

async def process_add_date(message: Message, state: FSMContext):
    if not check_date(message.text):
        await message.answer('❕ <i>Введена некорректная дата</i>')
        await state.finish()
        return
    await state.update_data(date=message.text)
    await AdminState.add_rating.set()
    await message.answer(text='📝 Введите оценку(0-10)...')

async def process_add_rating(message: Message, state: FSMContext):
    if not check_rating(message.text):
        await message.answer('❕ <i>Введена некорректная оценка</i>')
        await state.finish()
        return
    await state.update_data(rating=message.text)
    await AdminState.add_customer.set()
    await message.answer(text='📝 Введите покупателя...')

async def process_add_customer(message: Message, state: FSMContext):
    await state.update_data(customer=message.text)
    await AdminState.add_review.set()
    await message.answer(text='📝 Введите отзыв...')

async def process_add_review(message: Message, state: FSMContext):
    data = await state.get_data()
    add_review(date=data['date'], rating=data['rating'], customer=data['customer'], review=message.text)
    await message.answer(text='✔️ Отзыв успешно добавлен')
    await state.finish()

async def process_del_review_button(callback: CallbackQuery):
    reviews = get_reviews()
    await AdminState.page.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(reviews=reviews, page=1, pages_amount=get_pages_amount(len(reviews)))
    await callback.message.edit_text(text='🔴 <b>Выберите отзыв, который хотите удалить: </b>', reply_markup=await create_pagination_kb(reviews, 1, get_pages_amount(len(reviews)), delete=True))

async def process_forward_button_admin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['page'] + 1 <= data['pages_amount']:
        await state.update_data(page=data['page']+1)
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=data['page'] + 1, pages_amount=data['pages_amount'], delete=True))
    else:
        await state.update_data(page=1)
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=1, pages_amount=data['pages_amount'], delete=True))
    await callback.answer()

async def process_backward_button_admin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['page'] - 1 > 0:
        await state.update_data(page=data['page']-1)
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=data['page'] - 1, pages_amount=data['pages_amount'], delete=True))
    else:
        await state.update_data(page=data['pages_amount'])
        await callback.message.edit_reply_markup(reply_markup=await create_pagination_kb(reviews=data['reviews'], page=data['pages_amount'], pages_amount=data['pages_amount'], delete=True))
    await callback.answer()

async def process_del_review(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del_review(data['reviews'][int(callback.data.split(':')[1])])
    await callback.message.edit_text(text='✔️ Отзыв успешно удален')
    await state.finish()
    await callback.answer()

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, IDFilter(CFG.admin_ids), commands='admin', state='*')
    dp.register_callback_query_handler(process_cancel_button, text='cancel', state='*')
    dp.register_callback_query_handler(process_add_city_button, text='add_city')
    dp.register_message_handler(process_write_city, state=AdminState.add_city)
    dp.register_message_handler(process_add_operator, state=AdminState.add_operator)
    dp.register_callback_query_handler(process_add_good_button, text='add_good')
    dp.register_message_handler(process_write_good, state=AdminState.add_good)
    dp.register_message_handler(process_write_price, state=AdminState.add_price)
    dp.register_callback_query_handler(process_add_good_in_city_button, text='add_good_in_city')
    dp.register_callback_query_handler(process_add_good_in_city, text_startswith='ed_city', state=AdminState.add_good_in_city)
    dp.register_callback_query_handler(process_update_stock_add, text_startswith='ed_good', state='*')
    dp.register_callback_query_handler(delete_city_button, text='delete_city')
    dp.register_callback_query_handler(process_delete_city, text_startswith='del_city')
    dp.register_callback_query_handler(delete_good_button, text='delete_good')
    dp.register_callback_query_handler(process_delete_good, text_startswith='del_good')
    dp.register_callback_query_handler(process_del_good_in_city_button, text='delete_good_in_city')
    dp.register_callback_query_handler(process_del_good_in_city, text_startswith='in_city', state=AdminState.del_good_in_city)
    dp.register_callback_query_handler(procecc_update_stock_del, text_startswith='put_away_good', state='*')
    dp.register_callback_query_handler(process_add_review_button, text='add_review')
    dp.register_message_handler(process_add_date, state=AdminState.add_date)
    dp.register_message_handler(process_add_rating, state=AdminState.add_rating)
    dp.register_message_handler(process_add_customer, state=AdminState.add_customer)
    dp.register_message_handler(process_add_review, state=AdminState.add_review)
    dp.register_callback_query_handler(process_del_review_button, text='delete_review')
    dp.register_callback_query_handler(process_forward_button_admin, text='forward', state=AdminState.page)
    dp.register_callback_query_handler(process_backward_button_admin, text='backward', state=AdminState.page)
    dp.register_callback_query_handler(process_del_review, text_startswith='del_review', state=AdminState.page)
