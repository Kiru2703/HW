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
    
    # Dynamically grab whatever fields are sent, with fallback defaults
    task_title = data.get("title", data.get("task", "General Task Update"))
    priority = data.get("priority", "Normal")
    assignee = data.get("assignee", "Unassigned")
    bucket = data.get("bucket", data.get("category", "General"))
    status = data.get("status", "Active")
    notes = data.get("notes", data.get("description", ""))

    # Build a rich, comprehensive message containing everything
    desc_lines = [
        f"> **Category:** {bucket}",
        f"> **Priority:** {priority}",
        f"> **Assigned To:** {assignee}",
        f"> **Status:** {status}"
    ]
    if notes:
        desc_lines.append(f"\n**Details:** {notes}")

    discord_payload = {
        "content": f"📋 **Task Update: {task_title}**\n" + "\n".join(desc_lines)
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
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        return jsonify({"status": "failed", "error": f"HTTP {e.code}: {error_message}"}), 400
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
