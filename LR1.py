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
	
	if func == 'delete':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		bot.send_message(call.message.chat.id, 'Выберите номер напомниалки для удаления:')
		global info
		
		bot.send_message(call.message.chat.id, ''.join(info))
		
		bot.register_next_step_handler(call.message, delete_function)
	
	
def continue1(chat_id):
	bot.send_message(message.chat.id, '11')
	
		
def add_function(message):
	global info
	mes = message.text
	mes = mes.lstrip()
	
	data = mes[0:10]
	text = mes[10:len(mes)].lstrip()
	print(data, text)
	
	info.append('\n' + str(len(info)+1) + ' ' + data + ' ' + text)
	
	bot.send_message(message.chat.id, 'Успешно!')
	start(message)
	
def delete_function(message):
	global info
	mes = message.text
	
	info.pop(int(mes)-1)
	
	print(info)
	bot.send_message(message.chat.id, 'Успешно!')
	start(message)
	
def remind():
	now = datetime.now()
	current_time = now.strftime("%d.%m.%Y %H:%M:%S")
	print("Now =", current_time)
	
	date = now.strftime("%d.%m")
	print(date)
	
	global info
	text = ''.join(info)
	
	if date in text:
		print(date)
		print(''.join(info))
		
while True:
	if info != []:
	   remind()
	   sleep(1)

	
bot.polling(none_stop = True, interval = 0)
