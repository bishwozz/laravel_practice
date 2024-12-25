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

def main():
    url = "https://app.tweetscout.io/"
    follower_threshold = 5000  # Example threshold for minimum followers
    engagement_threshold = 5.0  # Example threshold for engagement rate (%)
    activity_threshold = 7.0  # Example threshold for activity score

    print(f"[{datetime.now()}] Fetching Twitter audience data...")
    audience_data = fetch_twitter_audience_data(url)

    print(f"[{datetime.now()}] Filtering influencers and active traders...")
    influencers = filter_influencers(audience_data, follower_threshold, engagement_threshold, activity_threshold)

    if influencers:
        print(f"[{datetime.now()}] Displaying promising influencers and active traders...")
        display_influencers(influencers)
    else:
        print(f"[{datetime.now()}] No promising influencers or active traders found.")

if __name__ == "__main__":
    main()
