import telebot

API_TOKEN = '6565230876:AAEQStltK-kZOuG--0uTYqCjcceM93IRtfE'  # Замените на токен вашего бота
ADMIN_ID = '1346861393'  # Замените на ID целевого пользователя (админа)

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения ID пользователей
user_ids = {}

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привет! Пожалуйста, напиши о своей задаче.")
    print('Пользователь приветствован и запрашивается информация о задаче.')

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def handle_user_message(message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids[user_id] = message.chat.id  # Сохраняем ID чата пользователя

    # Получаем имя пользователя или используем полное имя
    username = message.from_user.username
    user_link = f"@{username}" if username else message.from_user.full_name

    # Пересылаем сообщение от пользователя администратору
    bot.send_message(ADMIN_ID, f"Сообщение от пользователя {user_link} (ID: {user_id}): {message.text}")
    print(f'Сообщение от пользователя {user_link} переслано администратору.')

@bot.message_handler(func=lambda message: message.from_user.id == int(ADMIN_ID))
def handle_admin_message(message):
    if message.text.startswith('/answer'):
        # Извлекаем ID пользователя и текст ответа
        parts = message.text.split(' ', 2)  # Разделяем на части
        if len(parts) == 3:
            try:
                user_id = int(parts[1])  # Получаем ID пользователя
                response_text = parts[2]  # Получаем текст ответа
                
                # Проверяем, есть ли такой пользователь
                if user_id in user_ids:
                    bot.send_message(user_ids[user_id], f"Ответ от администратора {message.from_user.full_name}: {response_text}")
                    print(f'Ответ от админа был отправлен пользователю с ID {user_id}.')
                else:
                    bot.send_message(ADMIN_ID, "Пользователь с таким ID не найден.")
            except ValueError:
                bot.send_message(ADMIN_ID, "ID пользователя должен быть числом.")
        else:
            bot.send_message(ADMIN_ID, "Использование: /answer <user_id> <текст ответа>")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте команду /answer для ответа на сообщения пользователей.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
