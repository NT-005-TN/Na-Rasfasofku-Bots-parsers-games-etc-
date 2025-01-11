import telebot;
from telebot import types
import sqlite3
from fnmatch import *

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');

@bot.message_handler(commands=['start'])
def get_message(message):
	bot.send_message(message.chat.id, '1')
	
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
	file_path = 'C:/Users/Владимир/Desktop/ТелеграмБот/Под хранение'
	file_info = bot.get_file(message.photo[0].file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	src = file_path + message.photo[0].file_id
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
		
bot.polling(none_stop = True, interval = 0)
