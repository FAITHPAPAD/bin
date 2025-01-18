import logging
import rstr
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Initialize variables
generated_Bins = []
admin_id = "6830887977"  # Replace with your admin user ID
bot_token = "7748076089:AAGuiDwnRgDNvlcwQcegfaeyg-m0jQT6KzQ"  # Replace with your bot token

# Logging for telegram bot
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
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_Bin, Bin) for Bin in generated_Bins]
        executor.shutdown(wait=True)

def genetator(no, type):
    if type == "Mastercard":
        for i in range(no):
            gen_Bin().Mastercard()
        Thread(target=run1).start()

    elif type == "Visa":
        for i in range(no):
            gen_Bin().Visa()
        Thread(target=run1).start()

    elif type == "Amex":
        for i in range(no):
            gen_Bin().Amex()
        Thread(target=run1).start()

    elif type == "Discover":
        for i in range(no):
            gen_Bin().Discover()
        Thread(target=run1).start()

# Command handlers for the Telegram bot
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == int(admin_id):  # Check if the user is the admin
        update.message.reply_text("Welcome Admin! You can control the bin generator here.")
    else:
        update.message.reply_text("Welcome User! Only Admin can generate bins.")

def generate_bins(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == int(admin_id):  # Only allow admin to generate bins
        try:
            no_of_bins = int(context.args[0])  # Get number of bins from command arguments
            bin_type = context.args[1].capitalize()  # Get card type (Mastercard, Visa, etc.)
            
            if bin_type not in ["Mastercard", "Visa", "Amex", "Discover"]:
                update.message.reply_text("Invalid card type! Use Mastercard, Visa, Amex, or Discover.")
                return

            generated_Bins.clear()
            genetator(no_of_bins, bin_type)
            update.message.reply_text(f"Generating {no_of_bins} {bin_type} bins...")

        except (IndexError, ValueError):
            update.message.reply_text("Usage: /generate <number_of_bins> <card_type> (e.g., /generate 10 Mastercard)")

def save_bins(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == int(admin_id):
        file_path = f"Results/bins_{x.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(file_path, 'w') as file:
            for bin_code in generated_Bins:
                file.write(f"{bin_code}\n")
        update.message.reply_text(f"Bins saved to {file_path}")
    
def main():
    # Create Updater and Dispatcher for Telegram bot
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('generate', generate_bins))
    dispatcher.add_handler(CommandHandler('save', save_bins))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
