import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your Discord Webhook URL
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1560909813414895707/YRmAbNAIN7sCE0dDCKwlaxxbmvrGcIFFKz3LE2i3vzWHjOmzIXXZFRfojskYH0znelX3")

@app.route("/", methods=["GET"])
def home():
    return "Hardware Unit Bot is active!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    
    # Extract task details sent to this endpoint
    task_title = data.get("title", "New Task")
    priority = data.get("priority", "Normal")
    assignee = data.get("assignee", "Unassigned")
    bucket = data.get("bucket", "General")

    # Format the Discord embed payload
    payload = {
        "embeds": [
            {
                "title": f"📋 Task Update: {task_title}",
                "description": f"**Category:** {bucket}\n**Priority:** {priority}\n**Assigned To:** {assignee}",
                "color": 3447003,
                "footer": {"text": "TA Hardware Unit • Sync Bot"}
            }
        ]
    }

    # Push to Discord
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    
    if response.status_code == 204:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failed", "error": response.text}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))