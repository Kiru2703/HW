import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/", methods=["GET"])
def home():
    return "Hardware Unit Bot is active!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    
    task_title = data.get("title", "New Task")
    priority = data.get("priority", "Normal")
    assignee = data.get("assignee", "Unassigned")
    bucket = data.get("bucket", "General")

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

    # Added headers so Discord doesn't block the cloud server IP
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
    
    if response.status_code in [200, 204]:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failed", "error": response.text}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
