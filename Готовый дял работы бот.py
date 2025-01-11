import telebot

API_TOKEN = '6565230876:AAEQStltK-kZOuG--0uTYqCjcceM93IRtfE'  # Замените на токен вашего бота
ADMIN_ID = '1346861393'  # Замените на ID целевого пользователя (админа)
ADMIN_PASSWORD = '08-12-2006-18-66'  # Замените на ваш пароль для режима администратора

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения ID пользователей и их статуса
user_ids = {}
admin_mode = {}

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привет! Пожалуйста, напиши о своей задаче.")
    print('Пользователь приветствован и запрашивается информация о задаче.')

@bot.message_handler(commands=['admin'])
def cmd_admin(message):
    if message.text.split()[-1] == ADMIN_PASSWORD:
        admin_mode[message.from_user.id] = True
        bot.send_message(message.chat.id, "Вы вошли в режим администратора.")
        print(f'Администратор {message.from_user.id} вошел в режим администратора.')
    else:
        bot.send_message(message.chat.id, "Неверный пароль.")
        print(f'Попытка входа в режим администратора с неверным паролем от пользователя {message.from_user.id}.')

@bot.message_handler(commands=['notadmin'])
def cmd_notadmin(message):
    if message.from_user.id in admin_mode:
        del admin_mode[message.from_user.id]
        bot.send_message(message.chat.id, "Вы вышли из режима администратора.")
        print(f'Администратор {message.from_user.id} вышел из режима администратора.')

@bot.message_handler(commands=['answer'])
def cmd_answer(message):
    if message.from_user.id in admin_mode:
        try:
            # Извлекаем ID пользователя и текст сообщения
            _, user_id_str, *reply_message = message.text.split()
            user_id = int(user_id_str)
            reply_text = ' '.join(reply_message)

            if user_id in user_ids:
                # Отправляем ответ пользователю
                bot.send_message(user_ids[user_id], f"Ответ от администратора {message.from_user.full_name}: {reply_text}")
                bot.send_message(message.chat.id, f"Сообщение отправлено пользователю с ID {user_id}.")
                print(f'Ответ от администратора отправлен пользователю с ID {user_id}.')
            else:
                bot.send_message(message.chat.id, "Пользователь с таким ID не найден.")
        except (ValueError, IndexError):
            bot.send_message(message.chat.id, "Использование: /answer ID текст_сообщения")
    else:
        bot.send_message(message.chat.id, "Вы не находитесь в режиме администратора.")

@bot.message_handler(func=lambda message: True)
def handle_user_message(message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids[user_id] = message.chat.id  # Сохраняем ID чата пользователя

    # Получаем имя пользователя или используем полное имя
    username = message.from_user.username
    user_link = f"@{username}" if username else message.from_user.full_name

    # Пересылаем сообщение от пользователя администратору
    if user_id not in admin_mode:
        bot.send_message(ADMIN_ID, f"Сообщение от пользователя {user_link} (ID: {user_id}): {message.text}")
        print(f'Сообщение от пользователя {user_link} переслано администратору.')
    else:
        bot.send_message(message.chat.id, "Вы не можете отправлять сообщения другим пользователям в режиме администратора.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
