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
	

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	
	if call.data == 'owner':
		add_information_about_owner(call.message)
		

def add_infomation_about_owner(message):
	markup = types.InlineKeyboardMarkup()
	
	button1 = types.InlineKeyboardButton(text = 'Имя контактного лица', callback_data = 'name_of_owner')
	button2 = types.InlineKeyboardButton(text = 'Номер телефона контактного лица', callback_data = 'phone_number_of_owner')
	button3 = types.InlineKeyboardButton(text = 'Нужна ли термосумка', callback_data = 'needing_termoBag')
	button4 = types.InlineKeyboardButton(text = 'Число заведений', callback_data = 'number_of_cafe')
	button5 = types.InlineKeyboardButton(text = 'Показать введенные данные', callback_data = 'look_at_info_owner')
	button6 = types.InlineKeyboardButton(text = 'Завершить ввод', callback_data = 'end_of_adding_owner')
	button7 = types.InlineKeyboardButton(text = 'Удалить профиль', callback_data = 'delete_info_about_owner')
	
	markup.add(button1)
	markup.add(button2)
	markup.add(button3)
	markup.add(button4)
	markup.add(button5)
	markup.add(button6)
	markup.add(button7)
	
	bot.send_message(message.chat.id, "Выберите, что хотите ввести".format(message.from_user), reply_markup=markup)

	
	
bot.polling(none_stop = True, interval = 0)
