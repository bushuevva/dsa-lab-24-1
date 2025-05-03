# Импорт необходимых модулей
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command 
from aiogram.fsm.context import FSMContext 
from aiogram.fsm.state import State, StatesGroup 
from aiogram.types import Message 
from dotenv import load_dotenv 

# Загрузка переменной окружения
load_dotenv()

# Получение токена бота из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)  
dp = Dispatcher()

# Словарь для хранения курсов валют
currency_data = {}

# Класс для определения состояний бота
class CurrencyStates(StatesGroup):

    # Состояния для команды /save_currency
    waiting_for_currency = State()
    waiting_for_rate = State()
    
    # Состояния для команды /convert
    waiting_for_convert_currency = State() 
    waiting_for_convert_amount = State() 

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Приветственное сообщение со списком доступных команд"""
    await message.answer(
        "Привет! Я бот для работы с валютами. Мой создатель -\n студентка группы ФБИ-24 Бушуева Ирина\n"
        "Я могу выполнять следующие команды:\n"
        "/save_currency - Сохранить курс\n"
        "/convert - Конвертировать в рубли\n"
        "/courses - Показать курсы"
    )

# Обработчик команды /courses
@dp.message(Command("courses"))
async def cmd_courses(message: Message):
    """Показывает все сохраненные курсы валют"""
    if not currency_data:
        await message.answer("Нет сохранённых курсов")
        return
    # Формирование строки с курсами валют
    courses = "\n".join(f"{curr}: {rate} RUB" for curr, rate in currency_data.items())
    await message.answer(f"Текущие курсы:\n{courses}")

# Обработчик команды /save_currency
@dp.message(Command("save_currency"))
async def cmd_save_currency(message: Message, state: FSMContext):
    """Запрашивает название валюты для сохранения"""
    await message.answer("Введите название валюты (например, USD, EUR):")
    # Состояние ожидания ввода валюты
    await state.set_state(CurrencyStates.waiting_for_currency)

# Обработчик ввода названия валюты
@dp.message(CurrencyStates.waiting_for_currency)
async def process_currency(message: Message, state: FSMContext):
    """Проверяет и сохраняет название валюты, запрашивает курс"""
    # Преобразование к верхнему регистру
    currency = message.text.upper()
    # Проверка формата валюты
    if not currency.isalpha() or len(currency) != 3:
        await message.answer("Название валюты должно состоять из трех букв (например, EUR)")
        return
    # Сохраняем валюту во временное хранилище состояния
    await state.update_data(currency=currency)
    await message.answer(f"Введите курс {currency} к рублю:")
    # Cостояние ожидания ввода курса
    await state.set_state(CurrencyStates.waiting_for_rate)

# Обработчик ввода курса валюты
@dp.message(CurrencyStates.waiting_for_rate)
async def process_rate(message: Message, state: FSMContext):
    """Сохраняет курс валюты и завершает диалог"""
    try:
        # Получаем данные из состояния
        data = await state.get_data()
        currency = data['currency']
        # Преобразование введенного текста в число
        rate = float(message.text)
        # Сохраняем курс в глобальный словарь
        currency_data[currency] = rate
        await message.answer(f"✅ {currency} = {rate} RUB\nВсе курсы: {currency_data}")
    except ValueError:
        await message.answer("Ошибка! Введите число для курса.")
        return
    
    # Сбрасываем состояние
    await state.clear()


# Обработчик команды /convert (начало диалога)
@dp.message(Command("convert"))
async def cmd_convert(message: Message, state: FSMContext):
    """Запрашивает валюту для конвертации"""
    if not currency_data:
        await message.answer("Нет курсов. Добавьте через /save_currency")
        return
    # Показываем список доступных валют
    await message.answer(
        f"Введите валюту для конвертации:\nДоступно: {', '.join(currency_data.keys())}"
    )
    # Cостояние ожидания выбора валюты
    await state.set_state(CurrencyStates.waiting_for_convert_currency)

# Обработчик выбора валюты для конвертации
@dp.message(CurrencyStates.waiting_for_convert_currency)
async def process_convert_currency(message: Message, state: FSMContext):
    """Проверяет валюту и запрашивает сумму для конвертации"""
    currency = message.text.upper()
    if currency not in currency_data:
        await message.answer("Валюта не найдена. Пожалуйста, попробуйте ещё раз")
        return
    
    # Сохраняем выбранную валюту во временное хранилище
    await state.update_data(convert_currency=currency)
    await message.answer(f"Введите сумму в {currency}:")
    # Cостояние ожидания ввода суммы
    await state.set_state(CurrencyStates.waiting_for_convert_amount)

# Обработчик ввода суммы для конвертации
@dp.message(CurrencyStates.waiting_for_convert_amount)
async def process_convert_amount(message: Message, state: FSMContext):
    """Вычисляет и показывает результат конвертации"""
    try:
        data = await state.get_data()
        currency = data['convert_currency']
        amount = float(message.text)
        # Вычисляем результат
        result = amount * currency_data[currency]
        # Отправляем результат пользователю
        await message.answer(
            f"{amount} {currency} = {round(result, 2)} RUB "
            f"(1 {currency} = {currency_data[currency]} RUB)"
        )
    except ValueError:
        await message.answer("Ошибка! Введите число.")
        return
    
    # Сбрасываем состояние
    await state.clear()

import asyncio
print("Бот запущен...")
asyncio.run(dp.start_polling(bot))