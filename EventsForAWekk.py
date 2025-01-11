import telebot
import datetime
import sqlite3
from telebot import types
import logging

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');

events = {}  # хранилище событий

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Просмотреть список событий', 'Добавить событие', 'Удалить событие')
    bot.send_message(message.chat.id, 'Добро пожаловать в бот для напоминаний!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Просмотреть список событий':
        view_events(message)
    elif message.text == 'Добавить событие':
        add_event(message)
    elif message.text == 'Удалить событие':
        delete_event(message)
    else:
        if 'add_event' in bot.user_data[message.chat.id]:
            add_event_text(message)
        elif 'delete_event' in bot.user_data[message.chat.id]:
            delete_event_text(message)

def add_event(message):
    bot.send_message(message.chat.id, 'Введите событие в формате дд-mm-yyyy текст события')
    bot.user_data[message.chat.id] = {'add_event': True}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Отмена')
    bot.send_message(message.chat.id, 'Введите событие:', reply_markup=markup)

def add_event_text(message):
    if message.text == 'Отмена':
        bot.user_data.pop(message.chat.id, None)
        start_message(message)
    else:
        try:
            date_str, event_text = message.text.split(' ', 1)
            date = datetime.strptime(date_str, '%d-%m-%Y')
            if date > datetime.now() + timedelta(days=30):
                bot.send_message(message.chat.id, 'Дата должна быть не позднее 30 дней от текущей даты')
                return
            events[date_str] = event_text
            bot.send_message(message.chat.id, 'Событие добавлено!', reply_markup=start_markup(message.chat.id))
            bot.user_data.pop(message.chat.id, None)
        except ValueError:
            bot.send_message(message.chat.id, 'Неверный формат даты. Используйте формат дд-mm-yyyy')

def view_events(message):
    event_list = ''
    for i, (date, text) in enumerate(events.items(), 1):
        event_list += f'{i}. {date}: {text}\n'
    bot.send_message(message.chat.id, event_list, reply_markup=start_markup(message.chat.id))

def delete_event(message):
    bot.send_message(message.chat.id, 'Выберите номер события для удаления:')
    event_list = ''
    for i, (date, text) in enumerate(events.items(), 1):
        event_list += f'{i}. {date}: {text}\n'
    bot.send_message(message.chat.id, event_list)
    bot.user_data[message.chat.id] = {'delete_event': True}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Отмена')
    bot.send_message(message.chat.id, 'Введите номер события:', reply_markup=markup)

def delete_event_text(message):
    if message.text == 'Отмена':
        bot.user_data.pop(message.chat.id, None)
        start_message(message)
    else:
        try:
            event_num = int(message.text)
            date = list(events.keys())[event_num - 1]
            del events[date]
            bot.send_message(message.chat.id, 'Событие удалено!', reply_markup=start_markup(message.chat.id))
            bot.user_data.pop(message.chat.id, None)
        except (ValueError, IndexError):
            bot.send_message(message.chat.id, 'Неверный номер события')

def start_markup(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Просмотреть список событий', 'Добавить событие', 'Удалить событие')
    return markup

def remind_events():
    for date_str, event_text in events.items():
        date = datetime.strptime(date_str, '%d-%m-%Y')
        if date.date() == datetime.now().date():
            for chat_id in events:
                bot.send_message(chat_id, f'Напоминание: {event_text}')

bot.infinity_polling()

while True:
    remind_events()
    time.sleep(86400)  # 1 день в секундах
