import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# input bot token
SLACK_BOT_TOKEN = input("Enter your Slack Bot Token (xoxb-...): ").strip()
client = WebClient(token=SLACK_BOT_TOKEN)

# Prompt for channel ID and validate
while True:
    CHANNEL_ID = input("Enter the Channel ID to monitor: ").strip()
    try:
        client.conversations_info(channel=CHANNEL_ID)
        print(f"Channel ID {CHANNEL_ID} is valid!")
        break
    except SlackApiError as e:
        print(f"Invalid channel ID or bot not a member: {e.response['error']}. Try again.")

# Prompt for user ID to tag
USER_ID = input("Enter the User ID to tag on alert: ").strip()

# Keywords to detect in messages
KEYWORDS = ["integration", "app", "webhook"]  # You can also prompt if you want
POLL_INTERVAL = 10  # seconds

seen_messages = set()

def check_channel():
    try:
        response = client.conversations_history(channel=CHANNEL_ID, limit=20)
        messages = response.get("messages", [])
        for msg in reversed(messages):
            ts = msg.get("ts")
            text = msg.get("text", "").lower()
            if ts not in seen_messages:
                seen_messages.add(ts)
                for keyword in KEYWORDS:
                    if keyword.lower() in text:
                        alert_text = f"<@{USER_ID}> ⚠️ Possible integration added: {text}"
                        client.chat_postMessage(channel=CHANNEL_ID, text=alert_text)
                        print(f"Alert sent: {alert_text}")
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")

if __name__ == "__main__":
    print("Monitoring channel for integration-related messages...")
    while True:
        check_channel()
        time.sleep(POLL_INTERVAL)

