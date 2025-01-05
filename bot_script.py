import requests
from bs4 import BeautifulSoup

def fetch_meme_coin_data():
    """Scrape meme coin data from DexScreener's public webpage."""
    try:
        # URL for DexScreener meme coins (or any other valid page showing tokens)
        url = "https://www.dexscreener.com"  # Update with the exact page for meme coins
        
        # Adding headers to simulate a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meme_coins = []
        # Modify the selectors based on the actual page layout and structure
        # Replace 'div.token-class' and 'span.symbol' with the actual CSS selectors for the token sections
        for coin_section in soup.find_all('div', class_='token-class'):  # Update with correct class
            contract_address = coin_section.find('a', class_='contract-link')['href']
            token_symbol = coin_section.find('span', class_='symbol').text
            token_metadata = {"category": "meme", "chain": "ETH"}  # Example metadata (adjust accordingly)
            
            meme_coins.append({
                "contract_address": contract_address,
                "symbol": token_symbol,
                "metadata": token_metadata
            })

        return meme_coins
    except Exception as e:
        print(f"Error fetching meme coin data: {e}")
        return []

def forward_to_telegram(message):
    """Send the message to the Telegram bot."""
    TELEGRAM_BOT_URL = "https://api.telegram.org/bot8021090013:AAGXBr5Yu-dS0oMnXCA3epc-XXUFFeERRlU/sendMessage?chat_id=6217801019"
    payload = {"text": message}
    try:
        response = requests.post(TELEGRAM_BOT_URL, json=payload)
        response.raise_for_status()
        print("Message forwarded to Telegram bot successfully.")
    except Exception as e:
        print(f"Error forwarding message to Telegram bot: {e}")

def process_token(contract_address, token_symbol, token_metadata):
    """Process a token and forward data to Telegram."""
    print(f"Processing token: {token_symbol} ({contract_address})...")
    
    # Example of forwarding message to Telegram
    message = (
        f"Token found:\n"
        f"Contract Address: {contract_address}\n"
        f"Symbol: {token_symbol}\n"
        f"Metadata: {token_metadata}\n"
    )
    
    forward_to_telegram(message)

# Example usage
if __name__ == "__main__":
    meme_coins = fetch_meme_coin_data()
    
    if meme_coins:
        for coin in meme_coins:
            process_token(coin["contract_address"], coin["symbol"], coin["metadata"])
    else:
        print("No meme coins found or error occurred.")
