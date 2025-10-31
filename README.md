# 🧭 Integration Alert Bot

A Slack bot that alerts a specific user when a new **integration (bot)** joins a channel.

---

## 🚀 Features
- Listens for the `member_joined_channel` event.
- Detects when bots join and alerts a configured user.
- Easy setup with Flask and Slack Events API.

---

## ⚙️ Setup

### 1️⃣ Create a Slack App
1. Go to [Slack API – Create App](https://api.slack.com/apps).
2. Add **Event Subscriptions** → Enable events.
3. Request URL: `https://your-ngrok-url.ngrok.io/slack/events`
4. Subscribe to `member_joined_channel`.

### 2️⃣ Add OAuth Scopes
Under **OAuth & Permissions**:
channels:read
chat:write
users:read

### 3️⃣ Environment Variables
Create `.env` using `.env.example`:

