import telebot
import requests
from telebot import types

# Replace with your own bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)

def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]["usd"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btc_button = types.InlineKeyboardButton("Bitcoin", callback_data="bitcoin")
    eth_button = types.InlineKeyboardButton("Ethereum", callback_data="ethereum")
    ltc_button = types.InlineKeyboardButton("Litecoin", callback_data="litecoin")
    sol_button = types.InlineKeyboardButton("Solana", callback_data="solana")
    usdc_button = types.InlineKeyboardButton("USD Coin", callback_data="usd-coin")
    markup.add(btc_button, eth_button)
    markup.add(ltc_button, sol_button)
    markup.add(usdc_button)
    bot.send_message(message.chat.id, "Click the buttons to get the current prices for Bitcoin, Ethereum, Litecoin, Solana, and USD Coin.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["bitcoin", "ethereum", "litecoin", "solana", "usd-coin"])
def send_crypto_price(call):
    crypto_id = call.data
    crypto_name_map = {
        "bitcoin": "Bitcoin",
        "ethereum": "Ethereum",
        "litecoin": "Litecoin",
        "solana": "Solana",
        "usd-coin": "USD Coin"
    }
    crypto_name = crypto_name_map[crypto_id]
    price = get_crypto_price(crypto_id)
    bot.answer_callback_query(call.id, f"The current {crypto_name} price is *${price:,.2f}* USD.", show_alert=True)

if __name__ == '__main__':
    bot.polling()
