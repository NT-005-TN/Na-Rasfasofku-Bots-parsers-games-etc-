import telebot

API_TOKEN = '6565230876:AAEQStltK-kZOuG--0uTYqCjcceM93IRtfE'  # Replace with your bot token
ADMIN_ID = '1346861393'  # Replace with the ID of the target user (admin)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "Please enter the task description and subject in one message.")
    bot.register_next_step_handler(message, handle_task_and_subject)

def handle_task_and_subject(message):
    # Extract task description and subject from message
    try:
        parts = message.text.split(':', 1)
        if len(parts) != 2:
            raise ValueError("Invalid format. Please use 'Description:Subject'.")

        task_text, subject = parts
        task_text = task_text.strip()
        subject = subject.strip()

        # Save task description and subject
        user_name = message.from_user.full_name
        bot.send_message(ADMIN_ID, f"Task: {task_text}\nSubject: {subject}\nFrom: {user_name}")
        bot.send_message(message.chat.id, "Your task has been sent to the administrator. Waiting for a response.")

    except ValueError as e:
        bot.reply_to(message, f"Error: {e}")
        bot.register_next_step_handler(message, handle_task_and_subject)

@bot.message_handler(commands=['answer'])
def cmd_answer(message):
    if message.from_user.id != int(ADMIN_ID):
        bot.send_message(message.chat.id, "Only the administrator can use this command.")
        return

    try:
        parts = message.text.split(' ', 2)
        if len(parts) != 3:
            raise ValueError("Invalid format. Please use '/answer <user_id> <response_text'.")

        user_id, response_text = parts[1], parts[2]
        user_id = int(user_id)

        bot.send_message(user_id, f"Response from administrator: {response_text}")

    except ValueError as e:
        bot.reply_to(message, f"Error: {e}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
