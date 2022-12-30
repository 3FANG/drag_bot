from collections import namedtuple
from math import ceil
from datetime import datetime

from bot.database import select_query, insert_query, delete_query
from bot.database import connection


def get_cities():
    cities = [city[0] for city in select_query(connection, "SELECT name FROM City")]
    return cities

def get_goods(city: str=None):
    if city:
        goods = [(id, good, price) for id, good, price in select_query(connection, f"SELECT Good.id, name, price FROM Good JOIN Stock ON Good.id = Stock.good_id WHERE city_id = (SELECT id FROM City WHERE name = '{city}')")]
    else:
        goods = [(id, good, price) for id, good, price in select_query(connection, "SELECT id, name, price FROM Good")]
    return goods

def add_city(city: str, operator: str):
    insert_query(connection, 'INSERT INTO City(name, operator_link) VALUES (?,?)', (city, operator))

def add_good(name: str, price: str):
    insert_query(connection, 'INSERT INTO Good(name, price) VALUES (?,?)', (name, price))

def add_good_in_city(city: str, good_id: str):
    insert_query(connection, 'INSERT INTO Stock(city_id, good_id) VALUES ((SELECT id FROM City WHERE name = ?), ?)', (city, good_id))

def del_city(city: str):
    delete_query(connection, f"DELETE FROM City WHERE name = '{city}'")

def del_good(good_id: str):
    delete_query(connection, f"DELETE FROM Good WHERE id = {good_id}")

def del_good_from_city(city: str, good_id: int):
    delete_query(connection, f"DELETE FROM Stock WHERE good_id = {good_id} AND city_id = (SELECT id FROM City WHERE name = '{city}')")

def get_city_operator_link():
    operators = [(city, link) for city, link in select_query(connection, 'SELECT name, operator_link FROM City')]
    return operators

def get_price(good_id: int):
    name, price = select_query(connection, f"SELECT name, price FROM Good WHERE id = {good_id}")[0]
    return name, price

def get_reviews():
    reviews = namedtuple('reviews', 'id date rating customer review')
    reviews_list = [reviews(id, date, rating, customer, review) for id, date, rating, customer, review in select_query(connection, f"SELECT id, strftime('%d-%m-%Y', date), rating, customer, review FROM Review ORDER BY date DESC")]
    return reviews_list

def get_pages_amount(count_reviews: int):
    return ceil(count_reviews/10)

def get_review_text(review: namedtuple):
    months = {
        '1': 'Января',
        '2': 'Февраля',
        '3': 'Марта',
        '4': 'Апреля',
        '5': 'Мая',
        '6': 'Июня',
        '7': 'Июля',
        '8': 'Августа',
        '9': 'Сентября',
        '10': 'Октября',
        '11': 'Ноября',
        '12': 'Декабря'
    }
    day, month_num, year = review.date.split('-')
    text=f'''<b>Отзыв</b>
Дата: {day} {months[month_num]} {year} г.
Покупатель: {review.customer}
Оценка: {review.rating} из 10
Отзыв: {review.review}'''
    return text

def check_date(date: str):
    try:
        day, month, year = date.split('-')
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return False
        if not 0 < int(day) < 31 or not 0 < int(month) < 13 or int(year) < 2000:
            return False
        return True
    except:
        return False

def check_rating(num: str):
    if not num.isdigit() or not 0 <= int(num) < 11:
        return False
    return True

def add_review(date: str, rating: int, customer: str, review: str):
    insert_query(connection, "INSERT INTO Review(date, rating, customer, review) VALUES (?,?,?,?)", (f"{'-'.join(date.split('-')[::-1])} {datetime.now().strftime('%X')}", rating, customer, review))

def del_review(review: namedtuple):
    delete_query(connection, f"DELETE FROM Review WHERE id = {review.id}")

def check_user(id: int):
    answer = select_query(connection, f"SELECT EXISTS(SELECT id FROM User WHERE id = {id})")[0][0]
    return answer

def add_user(id: int, username: str):
    insert_query(connection, f"INSERT INTO User(id, username) VALUES(?,?)", (id, username))
