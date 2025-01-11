import telebot;
from telebot import types
import sqlite3

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');

@bot.message_handler(commands=['start'])
def command_start(message):
	markup = types.InlineKeyboardMarkup()
	
	add_information_about_deliver(message)
	
	'''
	button1 = types.InlineKeyboardButton(text = 'Я Курьер', callback_data = 'deliver')
	button2 = types.InlineKeyboardButton(text = 'Я Заказчик, мне нужны курьеры', callback_data = 'owner')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "Кто вы?".format(message.from_user), reply_markup=markup)
	
	
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == 'deliver':
		bot.send_message(call.message.chat.id, 'Заполните следующие данные')
		add_information_about_deliver()
	elif call.data == 'owner':
		print(2)
'''	

name = None
		
def add_information_about_deliver(message):
		connection = sqlite3.connect('info_about_deliver.sql')
		curs = connection.cursor()
		
		curs.execute('CREATE TABLE IF NOT EXISTS deliver (id String auto_increment primary key, name varchar(50))')
		connection.commit()
		curs.close()
		connection.close()
		
		bot.send_message(message.chat.id, 'Имя')
		bot.register_next_step_handler(message, user_name)
		
def user_name(message):
	global name
	name = message.text.strip()
	
	connection = sqlite3.connect('info_about_deliver.sql')
	curs = connection.cursor()
		
	curs.execute("INSERT INTO deliver (name) VALUES ('%s')" % (name))
	connection.commit()
	curs.close()
	connection.close()
	
	bot.send_message(message.chat.id, 'Чет еще')
	#bot.register_next_step_handler(message, user_next)
		
#def user_next(message):
	#next_text = message.text.strip()
	
	
		
		
bot.polling(none_stop = True, interval = 0)
