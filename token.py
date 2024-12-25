import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_twitter_audience_data(url):
    """Fetch Twitter audience data from the website."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    audience_data = []

    # Parsing logic (modify based on the website's actual structure)
    for row in soup.find_all('div', class_='audience-row'):
        try:
            username = row.find('span', class_='username').text.strip()
            followers = int(row.find('span', class_='followers').text.strip().replace(',', ''))
            engagement_rate = float(row.find('span', class_='engagement-rate').text.strip().replace('%', ''))
            activity_score = float(row.find('span', class_='activity-score').text.strip())
            audience_data.append({
                'username': username,
                'followers': followers,
                'engagement_rate': engagement_rate,
                'activity_score': activity_score
            })
        except Exception as e:
            print(f"Error parsing row: {e}")

    return audience_data

def filter_influencers(audience_data, follower_threshold, engagement_threshold, activity_threshold):
    """Filter influencers and active traders based on criteria."""
    influencers = []

    for audience in audience_data:
        if (audience['followers'] > follower_threshold and
                audience['engagement_rate'] > engagement_threshold and
                audience['activity_score'] > activity_threshold):
            influencers.append(audience)

    return influencers

def display_influencers(influencers):
    """Display the list of promising influencers and active traders."""
    print("\nPromising Influencers and Active Traders:\n")
    for influencer in influencers:
        print(f"Username: {influencer['username']}, Followers: {influencer['followers']}, Engagement Rate: {influencer['engagement_rate']}%, Activity Score: {influencer['activity_score']}")

def fetch_rugcheck_data(contract_address):
    """Fetch Rug Check data for a given contract address."""
    url = f"https://rugcheck.xyz/api/check?contract={contract_address}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Rug Check data: {response.status_code}")

    return response.json()

def validate_contract(data):
    """Validate the contract based on Rug Check data."""
    is_good = data.get('score') == 'Good'
    top_holder_percentage = data.get('top_holder_percentage', 100)

    return is_good and top_holder_percentage < 20  # Example threshold

def post_to_telegram(bot_token, chat_id, message):
    """Send a message to a Telegram bot."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.status_code}")

def main():
    twitter_url = "https://app.tweetscout.io/"
    follower_threshold = 5000  # Example threshold for minimum followers
    engagement_threshold = 5.0  # Example threshold for engagement rate (%)
    activity_threshold = 7.0  # Example threshold for activity score

    contract_address_list = ["0x123...", "0x456..."]  # Replace with real contract addresses
    bot_token = "INSERT_TELEGRAM_BOT_TOKEN"
    chat_id = "INSERT_TELEGRAM_CHAT_ID"

    print(f"[{datetime.now()}] Fetching Twitter audience data...")
    audience_data = fetch_twitter_audience_data(twitter_url)

    print(f"[{datetime.now()}] Filtering influencers and active traders...")
    influencers = filter_influencers(audience_data, follower_threshold, engagement_threshold, activity_threshold)

    if influencers:
        print(f"[{datetime.now()}] Displaying promising influencers and active traders...")
        display_influencers(influencers)

    print(f"[{datetime.now()}] Checking Rug Check data for contract addresses...")
    for contract_address in contract_address_list:
        try:
            rugcheck_data = fetch_rugcheck_data(contract_address)
            if validate_contract(rugcheck_data):
                message = f"Contract {contract_address} is valid with good Rug Check score."
                post_to_telegram(bot_token, chat_id, message)
                print(f"[{datetime.now()}] Alert sent for contract {contract_address}.")
            else:
                print(f"[{datetime.now()}] Contract {contract_address} is not valid.")
        except Exception as e:
            print(f"Error processing contract {contract_address}: {e}")

if __name__ == "__main__":
    main()
