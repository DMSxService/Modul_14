from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import my_token

api = my_token.my_token
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = InlineKeyboardMarkup(resize_keyboard=True)
kb2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
     InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
     InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
     InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')]
], resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button5 = KeyboardButton(text='Купить')
button2 = KeyboardButton(text='Информация')
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.add(button1, button2)
kb.add(button5)
kb1.add(button3, button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора для: '
                              'мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; '
                              'женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.',
                              reply_markup=types.ReplyKeyboardRemove())

    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:', reply_markup=types.ReplyKeyboardRemove())
    await call.answer()
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
    norm = int(data['weight']) * 10 + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма ккалорий в сутки: {norm}', reply_markup=kb)
    await state.finish()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'pictures/{i}.jpg', "rb") as img:
            await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена:{i * 100}',
                                 reply_markup=types.ReplyKeyboardRemove())
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.'
                         , reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
