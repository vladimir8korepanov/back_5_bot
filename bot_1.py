import telebot
import configparser

# Создаем объект ConfigParser
config = configparser.ConfigParser()
# Читаем конфигурационный файл
config.read('config.ini')

# Подключение к telegram api по токену
bot = telebot.TeleBot(config['bot']['token']) 

# Создание клавиатуры
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Часы', 'Минуты', 'Секунды')
input_type = 'Часы'

# Обработчик команд
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Этот бот умеет переводить время из часов в минуты и секунды и наоборот.')
    bot.send_message(message.chat.id, 'Выберите тип ввода:', reply_markup=keyboard)

# Обработчик сообщений
@bot.message_handler(func=lambda message: message.text in ['Часы', 'Минуты', 'Секунды'])
def handle_input_type(message):
    global input_type
    input_type = message.text
    
    # Запросите у пользователя значение
    bot.send_message(message.chat.id, f'Введите время ({input_type}):')
    
@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_input_value(message):
    value = float(message.text) 

    if input_type == 'Часы':
        hours = value
        minutes = value * 60
        seconds = value * 3600
    elif input_type == 'Минуты':
        hours = value / 60
        minutes = value
        seconds = value * 60
    elif input_type == 'Секунды':
        hours = value / 3600
        minutes = value / 60
        seconds = value
    # Отправка результата
    bot.send_message(message.chat.id, text=f'- {hours} часов\n- {minutes} минут\n- {seconds} секунд')

# Запуск бота
print('start')
bot.polling(none_stop = True)
