import requests
import schedule
import time
import tweepy

consumer_key = "[your-key]"
consumer_secret = "[your-secret]"
access_token = "[your-key]"
access_token_secret = "[your-secret]"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def fetch_data():
    query = """
    {
        transfers(
            first: 5
            orderBy:blockNumber
            orderDirection:desc
        ) {
            from
            to
            value
            transactionHash
            blockNumber
            blockTimestamp
        }
    }
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    request = requests.post(
        "https://gateway.thegraph.com/api/[FOX-API]/subgraphs/id/GvJCEpMuyymPEYJ8dLWvKFtBy1sz3bywdRSPzfY46MDR",
        headers=headers,
        json={"query": query}
    )

    data = request.json()
    transfers = data["data"]["transfers"]
    tweet_count = 0

    for transfer in transfers:
        if int(transfer['value']) >= 99999999999999999999999:
            transfer_value = "{:,.2f}".format(int(float(transfer['value'])) / 10**18)
            tweet_text = f"🚨🐋 Whale Alert! A transfer of {transfer_value} $FOX 🦊 was made from {transfer['from'][:4]}...{transfer['from'][-3:]} to {transfer['to'][:4]}...{transfer['to'][-3:]}. https://etherscan.com/tx/{transfer['transactionHash']} 🤖"
            api.update_status(tweet_text)
            tweet_count += 1
        if tweet_count >= 2:
            break

schedule.every().day.at("06:00").do(fetch_data)
schedule.every().day.at("12:00").do(fetch_data)
schedule.every().day.at("16:20").do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
