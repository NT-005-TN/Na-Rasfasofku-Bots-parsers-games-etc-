import telebot;
from telebot import types
import sqlite3

bot = telebot.TeleBot('7447269626:AAEHxc-qKe0kRYtULYQHts2leRmicKGNJIU');
name = None
phone_number = None
isTermoBag = None
transport = None

@bot.message_handler(commands=['start'])
def get_message(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Я Курьер', callback_data = 'deliver')
	button2 = types.InlineKeyboardButton(text = 'Я Заказчик, мне нужны курьеры', callback_data = 'owner')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "Кто вы?".format(message.from_user), reply_markup=markup)
	
	
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == 'deliver':
		bot.send_message(call.message.chat.id, 'Заполните следующие данные')
		add_information_about_deliver(call.message)
	elif call.data == 'owner':
		print(2)
	
		
def add_information_about_deliver(message):
	connection = sqlite3.connect('info_about_deliver.sql')
	curs = connection.cursor()
		
	curs.execute('CREATE TABLE IF NOT EXISTS deliver (id String auto_increment primary key, name varchar(50), phone_number varchar(12), isTermoBag varchar(4), transport varchar(50))')
	connection.commit()
	curs.close()
	connection.close()
		
	bot.send_message(message.chat.id, 'Имя')
	bot.register_next_step_handler(message, user_name)
	
def user_name(message):
	name = message.text.strip()
	
	bot.send_message(message.chat.id, 'Номер телефона')
	bot.register_next_step_handler(message, deliver_phone)
	
def deliver_phone(message):
	phone_number = message.text.strip()
	
	markup = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text = 'Да', callback_data = 'Yes')
	button2 = types.InlineKeyboardButton(text = 'Нет', callback_data = 'No')
	
	markup.add(button1)
	markup.add(button2)
	
	bot.send_message(message.chat.id, "У вас есть термосумка?".format(message.from_user), reply_markup=markup)
	

	
	
	
bot.polling(none_stop = True, interval = 0)
