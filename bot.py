import requests
import json
from bs4 import BeautifulSoup

# Telegram bot API URL (replace with the actual URL)
TELEGRAM_BOT_URL = "t.me/bis_drago_bot. "

# Thresholds
MIN_TWEETSCOUT_SCORE = 20
MAX_HOLDER_THRESHOLD = 20  # Top holder shouldn't hold more than 20% of the supply

def get_rugcheck_score(contract_address):
    """Check the RugCheck score for a contract."""
    url = f"https://rugcheck.xyz/contract/{contract_address}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()  # Assuming RugCheck provides JSON data
        return data.get("status", "").lower() == "good"
    except Exception as e:
        print(f"Error fetching RugCheck score for {contract_address}: {e}")
        return False

def get_tweetscout_score(token_symbol):
    """Check the TweetScout score for a token."""
    url = f"https://app.tweetscout.io/score/{token_symbol}"  # Adjust based on TweetScout's API or URL
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()  # Assuming TweetScout provides JSON data
        return data.get("score", 0) > MIN_TWEETSCOUT_SCORE
    except Exception as e:
        print(f"Error fetching TweetScout score for {token_symbol}: {e}")
        return False

def matches_meta(token_metadata, required_metadata):
    """
    Check if the token metadata matches the required criteria.
    Customize this function to match your specific meta requirements.
    """
    return all(token_metadata.get(key) == value for key, value in required_metadata.items())

def parse_html_contract_analysis(html_content):
    """
    Parse HTML content of the RugCheck response (if no API is available).
    Extracts status and holder information.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    status = soup.select_one(".contract-status").text.strip() if soup.select_one(".contract-status") else "Unknown"
    
    holders = []
    holder_rows = soup.select(".holder-row")  # Replace with actual selectors
    for row in holder_rows:
        try:
            holder = row.select_one(".holder-address").text.strip()
            percentage = float(row.select_one(".holder-percentage").text.strip().replace("%", ""))
            holders.append({"holder": holder, "percentage": percentage})
        except AttributeError:
            continue

    return {"status": status, "holders": holders}

def analyze_top_holders(holders):
    """
    Analyze if top holders hold too much of the supply.
    """
    for holder in holders:
        if holder["percentage"] > MAX_HOLDER_THRESHOLD:
            return False
    return True

def forward_to_telegram(message):
    """Send the message to the Telegram bot."""
    payload = {"text": message}
    try:
        response = requests.post(TELEGRAM_BOT_URL, json=payload)
        response.raise_for_status()
        print("Message forwarded to Telegram bot successfully.")
    except Exception as e:
        print(f"Error forwarding message to Telegram bot: {e}")

def process_token(contract_address, token_symbol, token_metadata, required_metadata):
    """Process a token based on the criteria."""
    print(f"Processing token: {token_symbol} ({contract_address})...")
    
    # Check RugCheck score
    rugcheck_good = get_rugcheck_score(contract_address)
    
    # Check TweetScout score
    tweetscout_good = get_tweetscout_score(token_symbol)
    
    # Check if metadata matches the current meta
    meta_matches = matches_meta(token_metadata, required_metadata)
    
    # Get holder data from RugCheck
    url = f"https://rugcheck.xyz/contract/{contract_address}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    holders_data = parse_html_contract_analysis(response.text)
    holders_ok = analyze_top_holders(holders_data["holders"])
    
    if rugcheck_good and tweetscout_good and meta_matches and holders_ok:
        message = (
            f"Token Approved for Minting:\n"
            f"Contract Address: {contract_address}\n"
            f"Symbol: {token_symbol}\n"
            f"Metadata: {json.dumps(token_metadata, indent=2)}\n"
            f"Top Holders: {json.dumps(holders_data['holders'], indent=2)}"
        )
        forward_to_telegram(message)
        print("Token meets criteria. Minting initiated.")
    else:
        print("Token does not meet criteria. Skipping.")

# Example usage
if __name__ == "__main__":
    # Example token data
    tokens = [
        {
            "contract_address": "0x123456789abcdef",
            "symbol": "TEST",
            "metadata": {"category": "meme", "chain": "ETH"}
        },
        {
            "contract_address": "0xabcdef123456789",
            "symbol": "MOON",
            "metadata": {"category": "utility", "chain": "BSC"}
        },
    ]
    
    # Required metadata criteria
    required_metadata = {"category": "meme", "chain": "ETH"}  # Example meta criteria

    for token in tokens:
        process_token(
            contract_address=token["contract_address"],
            token_symbol=token["symbol"],
            token_metadata=token["metadata"],
            required_metadata=required_metadata
        )
