import telebot
import gspread
from google.oauth2.service_account import Credentials

bot_token = '6151979814:AAEHKwPc7MzG-CeI82Re8UEMY_wNtuTUAjo'
google_keyfile = 'C:\project\client_secret.json'
sheet_link = 'https://docs.google.com/spreadsheets/d/15BlmG5T7bm0csZYxGimYsgeWec6Wh3de596dEA2i4J0/edit#gid=0'
google_sheetname = 'CompClub'
google_sheettab = 'List2'
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

bot = telebot.TeleBot(bot_token)

keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_status = telebot.types.KeyboardButton('/status')
button_reserve = telebot.types.KeyboardButton('/reserve')
keyboard.add(button_status, button_reserve)


def get_computers_status():
    creds = Credentials.from_service_account_file(google_keyfile, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(google_sheetname).worksheet(google_sheettab)

    data = sheet.get_all_values()

    computers_status = {}
    for row in data[1:]:
        computer_number = row[0]
        status = row[1]
        computers_status[computer_number] = status

    return computers_status

def update_computer_status(computer_number, status):
    creds = Credentials.from_service_account_file(google_keyfile, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(google_sheetname).worksheet(google_sheettab)

    data = sheet.get_all_values()

    for i, row in enumerate(data[1:], start=2):
        if row[0] == computer_number:
            sheet.update_cell(i, 2, status)
            break

@bot.message_handler(commands=['start'])
def start(message):
    
    bot.send_message(message.chat.id, "Привет! Чем могу помочь?", reply_markup=keyboard)

@bot.message_handler(commands=['status'])
def send_computers_status(message):
    computers_status = get_computers_status()

    response = "Статус компьютеров:\n\n"
    for computer_number, status in computers_status.items():
        response += f"Компьютер {computer_number}: {status}\n"

    bot.reply_to(message, response)

@bot.message_handler(commands=['reserve'])
def reserve_computer(message):
    params = message.text.split()
    if len(params) != 2:
        bot.reply_to(message, "Пожалуйста, используйте команду в формате: /reserve <номер компьютера>")
        return

    computer_number = params[1]
    computers_status = get_computers_status()

    if computer_number not in computers_status:
        bot.reply_to(message, f"Компьютер {computer_number} не существует")
        return

    if computers_status[computer_number] == 'Занят':
        bot.reply_to(message, f"Компьютер {computer_number} уже занят")
        return

    update_computer_status(computer_number, 'Занят')
    bot.reply_to(message, f"Компьютер {computer_number} успешно забронирован")

bot.polling()