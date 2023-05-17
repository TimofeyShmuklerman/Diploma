import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

bot_token = '6151979814:AAEHKwPc7MzG-CeI82Re8UEMY_wNtuTUAjo'

google_keyfile = 'C:\\project'
google_sheetname = 'CompClub'

bot = telebot.TeleBot(bot_token)

def get_computers_status():
    scope = ['https://docs.google.com/spreadsheets/d/1rv5YcyuKIHO86fVul-3QeBf3ywNWa32xIxv_ARgQyMw/edit?pli=1#gid=0', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_keyfile, scope)
    client = gspread.authorize(creds)
    sheet = client.open(google_sheetname).sheet1

    data = sheet.get_all_values()

    computers_status = {}
    for row in data[1:]:
        computer_number = row[0]
        status = row[1]
        computers_status[computer_number] = status

    return computers_status

@bot.message_handler(commands=['status'])
def send_computers_status(message):
    computers_status = get_computers_status()

    response = "Статус компьютеров:\n\n"
    for computer_number, status in computers_status.items():
        response += f"Компьютер {computer_number}: {status}\n"

    bot.reply_to(message, response)

bot.polling()