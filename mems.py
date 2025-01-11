import telebot;
from telebot import types
import sqlite3
from fnmatch import *
import os

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');
name = ''
choosed_type = ''
'''
@bot.message_handler(commands=['start'])
def start(message):
'''

types_of_memes = [
	'Игры','Коты'
	]

'''	
for x in types_of_memes:
	os.mkdir(x)
'''

@bot.message_handler(commands=['start'])
def start(message):
	global types_of_memes
	markup = types.InlineKeyboardMarkup()
	
	for x in types_of_memes:
		markup.add(types.InlineKeyboardButton(text = x, callback_data = x))
	
	bot.send_message(message.chat.id, "Выберите категорию мема: ".format(message.from_user), reply_markup=markup)
	
	
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global types_of_memes
	global choosed_type
	
	if call.data in types_of_memes:
		nextStep(call.message)
		choosed_type = call.data
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		print(choosed_type)
		
	if call.data == 'Add':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(call.message.chat.id, 'Отправьте мем')
		bot.register_next_step_handler(call.message, adding_mem)
		
	elif call.data == 'Choose':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(call.message.chat.id, 'Вот мемы:')
		choosing_mem(call.message)
		
@bot.message_handler(content_types=['document'])
def adding_mem(message):
	global choosed_type
	file_info = bot.get_file(message.photo[0].file_id)
	downloaded_file = bot.download_file(file_info.file_path)

	src = 'C:/Users/Владимир/Desktop/ТелеграмБот/Хранилище/'+ choosed_type + '/' + message.photo[0].file_id
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
	
	start(message)

def choosing_mem(message):
	global choosed_type
	directory = 'C:/Users/Владимир/Desktop/ТелеграмБот/Хранилище/'+ choosed_type
	files = os.listdir(directory)
	
	count = 0
	for x in files:
		bot.send_photo(message.chat.id, photo=open(directory+'/'+x, 'rb'))
		
		count += 1
		if count > 20:
			break
	
	start(message)
	
def nextStep(message):
	markup = types.InlineKeyboardMarkup()
	
	markup.add(types.InlineKeyboardButton(text = 'Добавить', callback_data = 'Add'))
	markup.add(types.InlineKeyboardButton(text = 'Выбрать', callback_data = 'Choose'))
	
	bot.send_message(message.chat.id, "Выберите действие: ".format(message.from_user), reply_markup=markup)
	
	
bot.polling(none_stop = True, interval = 0)


'''
for x in types_of_memes:
	markup.add(types.InlineKeyboardButton(text = x, callback_data = x))
	
bot.send_message(message.chat.id, "Выберите тип мемов: ".format(message.from_user), reply_markup=markup)
'''
