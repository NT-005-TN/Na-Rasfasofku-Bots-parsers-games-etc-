import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Установите ваш токен для Telegram бота
API_TOKEN = '6565230876:AAEQStltK-kZOuG--0uTYqCjcceM93IRtfE'

# Включаем логирование, чтобы видеть ошибки и сообщения
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Храним ключевые и минус-слова в глобальных переменных
KEYWORDS = ['important', 'urgent', 'help']  # Список ключевых слов по умолчанию
MINUS_KEYWORDS = ['spam', 'irrelevant', 'offensive']  # Минус-слова по умолчанию

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """
    Отправляет пользователю справку о доступных командах.
    """
    help_text = (
        "Я бот для фильтрации сообщений по ключевым и минус-словам.\n\n"
        "Доступные команды:\n"
        "/add_keywords <слова> - Добавить ключевые слова (через запятую).\n"
        "/add_minus_keywords <слова> - Добавить минус-слова (через запятую).\n"
        "/get_keywords - Получить список текущих ключевых слов.\n"
        "/get_minus_keywords - Получить список текущих минус-слов.\n"
        "/help - Показать это сообщение с описанием команд.\n\n"
        "Пример:\n"
        "/add_keywords important,urgent\n"
        "/add_minus_keywords spam,irrelevant\n"
    )
    await message.answer(help_text)

# Обработчик команд для добавления ключевых и минус-слов
@dp.message_handler(commands=['add_keywords'])
async def add_keywords(message: types.Message):
    """
    Пользователь может добавить ключевые слова с помощью команды.
    Пример: !add_keywords important,urgent
    """
    global KEYWORDS  # Объявляем KEYWORDS как глобальную переменную
    if message.text.startswith("/add_keywords "):
        keywords = message.text[len("/add_keywords "):].split(",")
        KEYWORDS.extend([keyword.strip() for keyword in keywords])
        await message.answer(f"Ключевые слова добавлены: {', '.join(keywords)}")

@dp.message_handler(commands=['add_minus_keywords'])
async def add_minus_keywords(message: types.Message):
    """
    Пользователь может добавить минус-слова с помощью команды.
    Пример: !add_minus_keywords spam,irrelevant
    """
    global MINUS_KEYWORDS  # Объявляем MINUS_KEYWORDS как глобальную переменную
    if message.text.startswith("/add_minus_keywords "):
        minus_keywords = message.text[len("/add_minus_keywords "):].split(",")
        MINUS_KEYWORDS.extend([keyword.strip() for keyword in minus_keywords])
        await message.answer(f"Минус-слова добавлены: {', '.join(minus_keywords)}")

# Обработчик команды для получения текущих списков ключевых и минус-слов
@dp.message_handler(commands=['get_keywords'])
async def get_keywords(message: types.Message):
    """
    Показывает список текущих ключевых слов.
    """
    await message.answer(f"Текущие ключевые слова: {', '.join(KEYWORDS)}")

@dp.message_handler(commands=['get_minus_keywords'])
async def get_minus_keywords(message: types.Message):
    """
    Показывает список текущих минус-слов.
    """
    await message.answer(f"Текущие минус-слова: {', '.join(MINUS_KEYWORDS)}")

# Обработчик загрузки файлов (TXT и JSON)
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file(message: types.Message):
    """
    Обрабатывает загрузку файла с ключевыми или минус-словами.
    """
    if message.document.mime_type == 'text/plain':
        global KEYWORDS, MINUS_KEYWORDS  # Объявляем как глобальные
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        # Скачиваем файл
        await bot.download_file(file_path, f'./{file.document.file_name}')
        
        with open(f'./{file.document.file_name}', 'r') as f:
            lines = f.readlines()
            keywords, minus_keywords = [], []
            for line in lines:
                line = line.strip()
                if line.startswith("KEYWORD:"):
                    keywords.append(line[len("KEYWORD:"):].strip())
                elif line.startswith("MINUS:"):
                    minus_keywords.append(line[len("MINUS:"):].strip())

            # Обновляем списки ключевых и минус-слов
            KEYWORDS.extend(keywords)
            MINUS_KEYWORDS.extend(minus_keywords)

        await message.answer("Файл обработан. Ключевые слова и минус-слова обновлены.")

    elif message.document.mime_type == 'application/json':
        global KEYWORDS, MINUS_KEYWORDS  # Объявляем как глобальные
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        # Скачиваем файл
        await bot.download_file(file_path, f'./{message.document.file_name}')
        
        # Чтение и обработка JSON файла
        with open(f'./{message.document.file_name}', 'r') as f:
            data = json.load(f)
            KEYWORDS.extend(data.get('keywords', []))
            MINUS_KEYWORDS.extend(data.get('minus_keywords', []))

        await message.answer("JSON файл обработан. Ключевые слова и минус-слова обновлены.")

# Фильтрация сообщений по ключевым и минус-словам
def filter_message(message: str) -> bool:
    """
    Фильтрует сообщение по ключевым и минус-словам.
    :param message: Сообщение для анализа.
    :return: True, если сообщение проходит фильтрацию, иначе False.
    """
    for word in MINUS_KEYWORDS:
        if word in message.lower():
            return False  # Сообщение содержит минус-слово, фильтруем его

    return any(keyword in message.lower() for keyword in KEYWORDS)

@dp.message_handler(content_types=['text'])
async def handle_message(message: types.Message):
    """
    Обрабатывает входящие сообщения.
    Если сообщение содержит ключевые слова и не содержит минус-слова,
    оно пересылается с ссылками на пользователя и сообщение.
    """
    if filter_message(message.text):
        user = message.from_user
        message_link = f'https://t.me/c/{message.chat.id}/{message.message_id}'  # Ссылка на сообщение
        user_link = f'https://t.me/{user.username}' if user.username else f'https://t.me/{user.id}'  # Ссылка на пользователя

        # Формируем ответное сообщение
        response = f"**Сообщение от {user.full_name}**: {message.text}\n"
        response += f"Ссылка на пользователя: {user_link}\n"
        response += f"Ссылка на сообщение: {message_link}"

        # Отправляем ответ
        await bot.send_message(message.chat.id, response, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
