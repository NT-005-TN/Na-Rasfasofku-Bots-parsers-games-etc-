import telebot
from telebot import types
import sqlite3
from fnmatch import *
from datetime import datetime 
from time import sleep

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');
info = []


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Создать', callback_data = 'add')
	button2 = types.InlineKeyboardButton(text = 'Удалить', callback_data = 'delete')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "Выберите действие с напоминалкой:".format(message.from_user), reply_markup=markup)
		
		
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	func = call.data
	
	if func == 'add':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		bot.send_message(call.message.chat.id, 'Введите дату в формате дд.мм.гггг и событие через пробел')
		bot.register_next_step_handler(call.message, add_function)
	
	
def add_function(message):
	1
		
bot.polling(none_stop = True, interval = 0)
