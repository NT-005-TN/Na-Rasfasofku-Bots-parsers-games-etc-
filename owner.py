import telebot;
from telebot import types
import sqlite3
from fnmatch import *

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');
name = ''
'''
@bot.message_handler(commands=['start'])
def start(message):
'''


#Разобраться с id и refresh_data Нужно хранить где-то прототип таблицы!

data = {}
info = {}	

@bot.message_handler(commands=['start'])
def start(message):
	connection = sqlite3.connect('users.sql')
	curs = connection.cursor()
	
	curs.execute('CREATE TABLE IF NOT EXISTS users (id String auto_increment primary key, name varchar(50), password varchar(50), count_of_money varchar(50), game_time varchar(50))')
	connection.commit()
		
	curs.close()
	connection.close()
	
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Авторизоваться', callback_data = 'autorize')
	button2 = types.InlineKeyboardButton(text = 'Регистрация', callback_data = 'register')
	markup.add(button1)
	markup.add(button2)
	bot.send_message(message.chat.id, "Выберите действие: ".format(message.from_user), reply_markup=markup)
	
	
	
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	refresh_data()
	
	if call.data == 'autorize':
		print('auto')
		
	elif call.data == 'register':
		bot.send_message(call.message.chat.id, 'Введите ваш никнейм')
		bot.register_next_step_handler(call.message, get_user_name)
		
	elif call.data == 'Yes':
		confirm_reg(call.message)
		
	elif call.data == 'No':
		bot.send_message(call.message.chat.id, 'Введите ваш никнейм')
		bot.register_next_step_handler(call.message, get_user_name)
		
	elif call.data == 'autorize':
		bot.send_message(call.message.chat.id, 'Введите ваш никнейм')
		bot.register_next_step_handler(call.message, autorize)
		
def autorize(message):
	global name
	name = message.text
	
	
	
	
	
	refresh_data()
	
		
def get_user_name(message):
	global name 
	name = message.text
	
	bot.send_message(message.chat.id, 'Введите ваш пароль')
	bot.register_next_step_handler(message, get_user_password)
	
def get_user_password(message):
	global info
	password = message.text
	info[name] = password
	
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Да', callback_data = 'Yes')
	button2 = types.InlineKeyboardButton(text = 'Нет', callback_data = 'No')
	markup.add(button1)
	markup.add(button2)
	bot.send_message(message.chat.id, 'Всё верно? ' + '\n' + name + '\n' + info[name].format(message.from_user), reply_markup=markup)
	
def confirm_reg(message):
	bot.delete_message(message.chat.id, message.message_id)
		
	global info
	connection = sqlite3.connect('users.sql')
	curs = connection.cursor()
		
	curs.execute("INSERT INTO users (name, password, count_of_money, game_time) VALUES ('%s', '%s','%s','%s')" % (name, info[name], '0', '0'))
	connection.commit()
		
	curs.execute('SELECT * FROM users')
	users = curs.fetchall()
	table = ''
	for el in users:
		table += str(el) + '\n'
		
	print('Данные таблицы >>>>>>>>>>>')
	print()
	print(table)
	print('Данные таблицы >>>>>>>>>>>')
	
	refresh_data()
	
	curs.close()
	connection.close()
	
def refresh_data():
	global data
	
	
	
	
bot.polling(none_stop = True, interval = 0)


'''
	
	connection = sqlite3.connect('info_about_deliver.sql')
	curs = connection.cursor()
	
	name, deliver_phone_number, isTermoBag, transport = information_about_deliver
	curs.execute("DELETE FROM deliver WHERE name = ('%s') AND phone_number = ('%s') AND isTermoBag = ('%s') AND  transport = ('%s')" % (name, deliver_phone_number, isTermoBag, transport))
	connection.commit()
		
	curs.close()
	connection.close()
		
	connection = sqlite3.connect('info_about_deliver.sql')
	curs = connection.cursor()
		
	name, deliver_phone_number, isTermoBag, transport = information_about_deliver
		
	curs.execute("INSERT INTO deliver (name, phone_number, isTermoBag, transport) VALUES ('%s', '%s','%s','%s')" % (name, deliver_phone_number, isTermoBag, transport))
	connection.commit()
		
	curs.execute('SELECT * FROM deliver')
	delivers = curs.fetchall()
	info = ''
	for el in delivers:
		info += str(el) + '\n'
		if el[1:].count('Нет данных') == 4:
			curs.execute("DELETE FROM deliver WHERE name = 'Нет данных' OR phone_number = 'Нет данных' OR isTermoBag = 'Нет данных' OR  transport = 'Нет данных'")
			connection.commit()
			print(el[1:], el[1:].count('Нет данных'))
		
	print('Данные таблицы >>>>>>>>>>>')
	print(info)
	print('Данные таблицы >>>>>>>>>>>')
		
	curs.close()
	connection.close()
	
	connection = sqlite3.connect('info_about_deliver.sql')
	curs = connection.cursor()
	
	curs.execute('CREATE TABLE IF NOT EXISTS deliver (id String auto_increment primary key, name varchar(50), phone_number varchar(12), isTermoBag varchar(6), transport varchar(50))')
	connection.commit()
		
	curs.close()
	connection.close()


'''
