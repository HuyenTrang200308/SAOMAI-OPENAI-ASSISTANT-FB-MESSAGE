import requests
from config import PAGE_ACCESS_TOKEN

FB_GRAPH_URL = "https://graph.facebook.com/v18.0/me/messages"

def send_text_message(recipient_id: str, message_text: str) -> None:
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    response = requests.post(FB_GRAPH_URL, params=params, json=data)
    print("📤 Gửi tin nhắn văn bản:", response.status_code, response.text)

def send_quick_reply(recipient_id: str, text: str, replies: list):
    quick_replies = [
        {"content_type": "text", "title": reply, "payload": reply}
        for reply in replies
    ]
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
            "quick_replies": quick_replies
        }
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    response = requests.post(FB_GRAPH_URL, params=params, json=data)
    print("📤 Gửi quick reply:", response.status_code, response.text)
    return response.json()

def send_button_message(recipient_id: str, text: str, zalo_url: str, hotline: str, extra_button: dict = None):
    """Gửi tin nhắn có tối đa 3 nút: Zalo OA, Gọi Hotline, và nút tùy chọn"""
    buttons = [
        {
            "type": "web_url",
            "url": zalo_url,
            "title": "💬 Nhắn Zalo OA"
        },
        {
            "type": "phone_number",
            "title": "📞 Gọi Hotline",
            "payload": hotline
        }
    ]

    if extra_button:
        buttons.append(extra_button)

    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        }
    }

    params = {"access_token": PAGE_ACCESS_TOKEN}
    response = requests.post(FB_GRAPH_URL, params=params, json=data)
    print("📤 Gửi button 3 nút:", response.status_code, response.text)
    return response.json()
