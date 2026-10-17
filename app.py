import os
import urllib.request
import json
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

    # Clean text message payload which bypasses embed blocks on strict IPs
    discord_payload = {
        "content": f"📋 **Task Update: {task_title}**\n> **Category:** {bucket}\n> **Priority:** {priority}\n> **Assigned To:** {assignee}"
    }

    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(discord_payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 204]:
                return jsonify({"status": "success"}), 200
            else:
                return jsonify({"status": "failed", "error": response.read().decode()}), 400
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
