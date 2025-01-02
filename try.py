import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Define constants for API keys and bot information
RUGCHECK_API_URL = "https://api.rugcheck.io/token"
TWEETSCOUT_API_URL = "https://api.tweetscout.com/token"
TELEGRAM_BOT_TOKEN = '8021090013:AAGXBr5Yu-dS0oMnXCA3epc-XXUFFeERRlU'
CHAT_ID = '6217801019'

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Function to fetch and analyze token using RugCheck
async def analyze_with_rugcheck(token_address):
    response = requests.get(f"{RUGCHECK_API_URL}?address={token_address}")
    if response.status_code == 200:
        data = response.json()
        if data.get('valid', False):  # Assuming 'valid' is part of the API response
            return True, data
    return False, None

# Function to fetch and analyze token using TweetScout
async def analyze_with_tweetscout(token_address):
    response = requests.get(f"{TWEETSCOUT_API_URL}?address={token_address}")
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'safe':  # Assuming 'safe' indicates a valid token
            return True, data
    return False, None

# Function to forward validated token to Telegram bot
async def forward_to_telegram(token_address, analysis_result):
    message = f"Token Address: {token_address}\nResult: {analysis_result}"
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Function to analyze token and validate it using RugCheck and TweetScout
async def analyze_token(token_address):
    # Analyze with RugCheck
    valid, result = await analyze_with_rugcheck(token_address)
    if valid:
        await forward_to_telegram(token_address, "Valid Token (RugCheck)")
        return

    # Analyze with TweetScout
    valid, result = await analyze_with_tweetscout(token_address)
    if valid:
        await forward_to_telegram(token_address, "Valid Token (TweetScout)")
        return

    # If neither are valid, notify about it
    await forward_to_telegram(token_address, "Invalid Token")

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Token Analyzer Bot! Use /analyze <token_address> to start analyzing.")

# Function to handle the /analyze command
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a token address to analyze. Example: /analyze <token_address>")
        return

    token_address = context.args[0]  # Token address passed as an argument
    await analyze_token(token_address)
    await update.message.reply_text(f"Analyzing token: {token_address}")

# Main function to run the bot
def main():
    # Set up the Telegram bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('analyze', analyze))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()