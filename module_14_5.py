from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

get_all_products()

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

ikb = InlineKeyboardMarkup(inline_keyboard=
                           [[InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
                             InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]],
                           resize_keyboard=True)

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'),
     KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить'),
     KeyboardButton(text='Регистрация')
     ]], resize_keyboard=True)

ikb2 = InlineKeyboardMarkup(inline_keyboard=
[[
    InlineKeyboardButton(text='Product1', callback_data="product_buying"),
    InlineKeyboardButton(text='Product2', callback_data="product_buying"),
    InlineKeyboardButton(text='Product3', callback_data="product_buying"),
    InlineKeyboardButton(text='Product4', callback_data="product_buying"),
]], resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) - 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(text='Информация')
async def b_info(message):
    await message.answer('Чтобы узнать норму каллорий, жми:"Рассчитать"')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {calories:.2f}')

    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    count = 1
    for product in products:
        with open(f'jpg{count}.jpg', 'rb') as img:
            await message.answer(
                f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}"
            )
            await message.answer_photo(img)

        count += 1

    await message.answer('Выберите продукт для покупки:', reply_markup=ikb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(massage, state):
    if not is_included(massage.text):
        await state.update_data(username=massage.text)
        await massage.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await massage.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data_u = await state.get_data()
    add_user(data_u['username'], data_u['email'], data_u['age'])
    await message.answer('Регистрация прошла успешно')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)