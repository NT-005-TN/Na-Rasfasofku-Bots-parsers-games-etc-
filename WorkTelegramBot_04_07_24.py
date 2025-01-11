import telebot;
from telebot import types
import sqlite3
from fnmatch import *

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');
information_about_deliver = ['Нет данных']*4


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Я Курьер', callback_data = 'deliver')
	button2 = types.InlineKeyboardButton(text = 'Я Заказчик, мне нужны курьеры', callback_data = 'owner')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "Кто вы?".format(message.from_user), reply_markup=markup)
	
	connection = sqlite3.connect('info_about_deliver.sql')
	curs = connection.cursor()
	
	curs.execute('CREATE TABLE IF NOT EXISTS deliver (id String auto_increment primary key, name varchar(50), phone_number varchar(12), isTermoBag varchar(6), transport varchar(50))')
	connection.commit()
		
	curs.close()
	connection.close()
	

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	start_deliver_part(call)



def start_deliver_part(call):
	global information_about_deliver
	
	if call.data == 'deliver':
		bot.delete_message(call.message.chat.id, call.message.message_id)
	
		bot.send_message(call.message.chat.id, 'Отредактируйте следующую информацию: ')
		add_information_about_deliver(call.message)
		
	elif call.data == 'owner':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		print('owner')
	
	elif call.data == 'name':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		bot.send_message(call.message.chat.id, 'Введите ваше имя')
		bot.register_next_step_handler(call.message, get_deliver_name)
		
	elif call.data == 'phone_number':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		bot.send_message(call.message.chat.id, 'Введите ваш номер телефона')
		bot.register_next_step_handler(call.message, get_deliver_phone_number)
		
	elif call.data == 'having_termoBag':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		get_info_about_bag(call.message)
		
	elif call.data == 'BagIsAvailable':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		information_about_deliver[2] = 'Есть'
		add_information_about_deliver(call.message)
	
	elif call.data == 'BagIsNotAvailable':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		information_about_deliver[2] = 'No'
		add_information_about_deliver(call.message)
	
	elif call.data == 'type_of_transport':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		get_info_about_transport(call.message)
		
	elif call.data == 'walking':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		information_about_deliver[3] = 'Пеший курьер'
		add_information_about_deliver(call.message)
	
	elif call.data == 'velo':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		information_about_deliver[3] = 'Велокурьер'
		add_information_about_deliver(call.message)
		
	elif call.data == 'moto':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		information_about_deliver[3] = 'Мотокурьер'
		add_information_about_deliver(call.message)
		
	elif call.data == 'avto':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		information_about_deliver[3] = 'Автокурьер'
		add_information_about_deliver(call.message)
	
	elif call.data == 'look_at_info':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		info = ''
		for x in information_about_deliver:
			info += str(x) + '\n'
			
		bot.send_message(call.message.chat.id, info)
		add_information_about_deliver(call.message)
		
	elif call.data == 'end_of_adding':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		
		info = ''
		for x in information_about_deliver:
			info += str(x) + '\n'
			
		bot.send_message(call.message.chat.id, info)
		if information_about_deliver.count('Нет данных') == 0:
			confirm_of_information(call.message)
		else:
			bot.send_message(call.message.chat.id, 'Заполните все данные и после этого завершите ввод данных')
			add_information_about_deliver(call.message)
		
		
	elif call.data == 'all_is_correct':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		#Function
		
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
		
		main_menu_of_deliver(call.message)
	
	elif call.data == 'edit':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		add_information_about_deliver(call.message)
	
	elif call.data == 'delete_info_about_deliver':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		bot.send_message(call.message.chat.id, '(чтобы удалить уже созданный аккаунт, нажмите "Я Курьер", после введите все ваши данные и нажмите удалить аккаунт)')
		
		connection = sqlite3.connect('info_about_deliver.sql')
		curs = connection.cursor()
			
		name, deliver_phone_number, isTermoBag, transport = information_about_deliver
		curs.execute("DELETE FROM deliver WHERE name = ('%s') AND phone_number = ('%s') AND isTermoBag = ('%s') AND  transport = ('%s')" % (name, deliver_phone_number, isTermoBag, transport))
		connection.commit()
		
		curs.close()
		connection.close()
			
		name, deliver_phone_number, isTermoBag, transport = ['Нет данных']*4
		information_about_deliver = ['Нет данных']*4
		
		start(call.message)	
		
def main_menu_of_deliver(message):
	print(1)

def confirm_of_information(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Все верно', callback_data = 'all_is_correct')
	button2 = types.InlineKeyboardButton(text = 'Нужно изменить', callback_data = 'edit')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "Данные введены коректно?".format(message.from_user), reply_markup=markup)
	
	
def get_info_about_transport(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Пеший курьер', callback_data = 'walking')
	button2 = types.InlineKeyboardButton(text = 'Велокурьер', callback_data = 'velo')
	button3 = types.InlineKeyboardButton(text = 'Мотокурьер', callback_data = 'moto')
	button4 = types.InlineKeyboardButton(text = 'Автокурьер', callback_data = 'avto')
	
	markup.add(button1)
	markup.add(button2)
	markup.add(button3)
	markup.add(button4)
	
	bot.send_message(message.chat.id, "Выберите ваш вид транспорта".format(message.from_user), reply_markup=markup)
	
		
def get_info_about_bag(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Есть', callback_data = 'BagIsAvailable')
	button2 = types.InlineKeyboardButton(text = 'Нет', callback_data = 'BagIsNotAvailable')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "У вас есть термосумка?".format(message.from_user), reply_markup=markup)
	

def get_deliver_name(message):
	name = message.text
	information_about_deliver[0] = name
	
	add_information_about_deliver(message)
	
def get_deliver_phone_number(message):
	phone_number = message.text
	
	if not fnmatch(phone_number, '+7??????????'):
		bot.send_message(message.chat.id, 'Введите ваш номер телефона в формате +79123456789')
		bot.register_next_step_handler(message, get_deliver_phone_number)
	else:
		information_about_deliver[1] = phone_number
		add_information_about_deliver(message)
	
	
	
def add_information_about_deliver(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Имя', callback_data = 'name')
	button2 = types.InlineKeyboardButton(text = 'Номер телефона', callback_data = 'phone_number')
	button3 = types.InlineKeyboardButton(text = 'Есть ли термосумка', callback_data = 'having_termoBag')
	button4 = types.InlineKeyboardButton(text = 'Вид транспорта', callback_data = 'type_of_transport')
	button5 = types.InlineKeyboardButton(text = 'Показать введенные данные', callback_data = 'look_at_info')
	button6 = types.InlineKeyboardButton(text = 'Завершить ввод', callback_data = 'end_of_adding')
	button7 = types.InlineKeyboardButton(text = 'Удалить профиль', callback_data = 'delete_info_about_deliver')
	
	markup.add(button1)
	markup.add(button2)
	markup.add(button3)
	markup.add(button4)
	markup.add(button5)
	markup.add(button6)
	markup.add(button7)
	
	bot.send_message(message.chat.id, "Выберите, что хотите ввести".format(message.from_user), reply_markup=markup)
	


bot.polling(none_stop = True, interval = 0)

