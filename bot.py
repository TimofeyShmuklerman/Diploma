import telebot
import gspread
from google.oauth2.service_account import Credentials

bot_token = '6151979814:AAEHKwPc7MzG-CeI82Re8UEMY_wNtuTUAjo'
sheet_link = 'https://docs.google.com/spreadsheets/d/15BlmG5T7bm0csZYxGimYsgeWec6Wh3de596dEA2i4J0/edit#gid=0'

google_keyfile = 'C:\project\client_secret.json'
google_sheetname = 'CompClub'
scope = ['https://www.googleapis.com/auth/spreadsheets', 
             'https://www.googleapis.com/auth/drive']

bot = telebot.TeleBot(bot_token)
# bot.set_webhook()

def get_computers_status():
    creds = Credentials.from_service_account_file(google_keyfile, scopes=scope)
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