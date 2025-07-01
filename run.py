from flask import Flask, request
from config import VERIFY_TOKEN
from main import handle_message, handle_quick_reply

app = Flask(__name__)

@app.route("/", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook xác thực thành công")
        return challenge, 200
    else:
        print("❌ Webhook xác thực thất bại")
        return "Xác thực thất bại", 403

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 DỮ LIỆU:", data)

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                message = event.get("message", {})
                text = message.get("text", "")
                quick_reply = message.get("quick_reply", {}).get("payload")

                print(f"👤 Từ: {sender_id} | Nội dung: {text} | QuickReply: {quick_reply}")

                if quick_reply:
                    handle_quick_reply(sender_id, quick_reply)
                elif text:
                    handle_message(sender_id, text)

    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
