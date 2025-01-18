import logging
import rstr
import requests
import datetime
from threading import Thread
import telebot
from concurrent.futures import ThreadPoolExecutor
import json
import time

# Initialize variables
generated_Bins = []
admin_id = "6830887977"  # Replace with your admin user ID
bot_token = "7748076089:AAGuiDwnRgDNvlcwQcegfaeyg-m0jQT6KzQ"  # Replace with your bot token
subscription_file = "subscriptions.json"  # File to store subscriptions

# Logging for telegram bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

x = datetime.datetime.now()

# Initialize bot
bot = telebot.TeleBot(bot_token)

# Load subscriptions from file
def load_subscriptions():
    try:
        with open(subscription_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save subscriptions to file
def save_subscriptions(subscriptions):
    with open(subscription_file, 'w') as file:
        json.dump(subscriptions, file, indent=4)

# Check if user is subscribed
def is_subscribed(user_id):
    subscriptions = load_subscriptions()
    if str(user_id) in subscriptions:
        subscription = subscriptions[str(user_id)]
        # Check if the subscription is still valid (e.g., check expiry time)
        if time.time() < subscription['expiry']:
            return True
    return False

# Add subscription for a user
def add_subscription(user_id, duration=86400):  # Duration in seconds (86400 = 1 day)
    subscriptions = load_subscriptions()
    expiry_time = time.time() + duration  # Set expiry time
    subscriptions[str(user_id)] = {"expiry": expiry_time}
    save_subscriptions(subscriptions)

# Remove subscription for a user
def remove_subscription(user_id):
    subscriptions = load_subscriptions()
    if str(user_id) in subscriptions:
        del subscriptions[str(user_id)]
        save_subscriptions(subscriptions)

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

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):  # Check if the user is subscribed
        bot.reply_to(message, "Welcome! You are subscribed and can use the bin generator.")
    else:
        bot.reply_to(message, "Welcome! You are not subscribed. Type /subscribe to start your subscription.")

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        bot.reply_to(message, "You are already subscribed!")
    else:
        # Add subscription for 1 day (86400 seconds)
        add_subscription(user_id, duration=86400)
        bot.reply_to(message, "You have been subscribed for 1 day! You can now use the bin generator.")

@bot.message_handler(commands=['generate'])
def generate_bins(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):  # Only allow subscribed users to generate bins
        try:
            args = message.text.split()
            no_of_bins = int(args[1])  # Get number of bins from command arguments
            bin_type = args[2].capitalize()  # Get card type (Mastercard, Visa, etc.)
            
            if bin_type not in ["Mastercard", "Visa", "Amex", "Discover"]:
                bot.reply_to(message, "Invalid card type! Use Mastercard, Visa, Amex, or Discover.")
                return

            generated_Bins.clear()
            genetator(no_of_bins, bin_type)
            bot.reply_to(message, f"Generating {no_of_bins} {bin_type} bins...")

        except (IndexError, ValueError):
            bot.reply_to(message, "Usage: /generate <number_of_bins> <card_type> (e.g., /generate 10 Mastercard)")
    else:
        bot.reply_to(message, "You are not subscribed! Type /subscribe to get access.")

@bot.message_handler(commands=['save'])
def save_bins(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):  # Only allow subscribed users to save bins
        file_path = f"Results\