import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# Initialize Slack app
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Configuration
channel_id = input("Enter the channel ID to monitor: ").strip()
user_id = input("Enter the user ID to tag: ").strip()

@app.event("member_joined_channel")
def handle_member_joined_channel(event, say):
    print(f"Event received: {event}")  # Debug logging
    channel = event.get("channel")
    inviter = event.get("inviter")
    
    if channel == channel_id:
        say(
            channel=channel,
            text=f"<@{user_id}> An integration or user was just added to <#{channel}> by <@{inviter}>!"
        )

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # Handle URL verification challenge
    data = request.get_json()
    if data and data.get("type") == "url_verification":
        print("Responding to URL verification challenge")
        return jsonify({"challenge": data.get("challenge")}), 200
    
    # Handle all other events
    return handler.handle(request)

@flask_app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    print("Bot is running...")
    print(f"Monitoring channel: {channel_id}")
    print(f"Will notify user: {user_id}")
    flask_app.run(port=3000, debug=True)
