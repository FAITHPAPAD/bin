import logging
import rstr
import requests
import datetime
import telebot

# Initialize variables
generated_Bins = []
admin_id = "6830887977"  # Replace with your admin user ID
bot_token = "7748076089:AAGuiDwnRgDNvlcwQcegfaeyg-m0jQT6KzQ"  # Replace with your bot token

# Initialize bot
bot = telebot.TeleBot(bot_token)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

x = datetime.datetime.now()

class gen_Bin:
    def Mastercard(self):
        generated_Bins.append(rstr.xeger(str(5) + "\d{5}"))

    def Visa(self):
        generated_Bins.append(rstr.xeger(str(4) + "\d{5}"))

    def Amex(self):
        generated_Bins.append(rstr.xeger(str(3) + "\d{5}"))

    def Discover(self):
        generated_Bins.append(rstr.xeger(str(6) + "\d{5}"))

def check_Bin(Bin):
    url = f"https://binlist.io/lookup/{Bin}"
    datas = requests.get(url).json()

    if datas['success'] == True:
        return f"Bin      :  {Bin}\n" \
               f"Scheme   :  {datas['scheme']}\n" \
               f"Country  :  {datas['country']['name']}\n" \
               f"Type     :  {datas['type']}\n" \
               f"Category :  {datas['category']}\n" \
               f"Bank     :  {datas['bank']['name']}\n________________________"
    return "Invalid Bin"

def run1():
    for Bin in generated_Bins:
        print(check_Bin(Bin))

def genetator(no, type):
    if type == "Mastercard":
        for i in range(no):
            gen_Bin().Mastercard()
        run1()

    elif type == "Visa":
        for i in range(no):
            gen_Bin().Visa()
        run1()

    elif type == "Amex":
        for i in range(no):
            gen_Bin().Amex()
        run1()

    elif type == "Discover":
        for i in range(no):
            gen_Bin().Discover()
        run1()

# Command handlers for the Telegram bot
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id == int(admin_id):  # Check if the user is the admin
        bot.reply_to(message, "Welcome Admin! You can control the bin generator here.")
    else:
        bot.reply_to(message, "Welcome User! Only Admin can generate bins.")

@bot.message_handler(commands=['generate'])
def generate_bins(message):
    user_id = message.from_user.id
    if user_id == int(admin_id):  # Only allow admin to generate bins
        try:
            args = message.text.split()[1:]
            no_of_bins = int(args[0])  # Get number of bins from command arguments
            bin_type = args[1].capitalize()  # Get card type (Mastercard, Visa, etc.)

            if bin_type not in ["Mastercard", "Visa", "Amex", "Discover"]:
                bot.reply_to(message, "Invalid card type! Use Mastercard, Visa, Amex, or Discover.")
                return

            generated_Bins.clear()
            genetator(no_of_bins, bin_type)
            bot.reply_to(message, f"Generating {no_of_bins} {bin_type} bins...")

        except (IndexError, ValueError):
            bot.reply_to(message, "Usage: /generate <number_of_bins> <card_type> (e.g., /generate 10 Mastercard)")

@bot.message_handler(commands=['save'])
def save_bins(message):
    user_id = message.from_user.id
    if user_id == int(admin_id):
        file_path = f"Results/bins_{x.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(file_path, 'w') as file:
            for bin_code in generated_Bins:
                file.write(f"{bin_code}\n")
        bot.reply_to(message, f"Bins saved to {file_path}")

# Start polling to handle messages
bot.polling(none_stop=True)
