import requests

import config

def send_message_to_fb_messenger(recipinet_id: str, message_text: str) -> None:
    url = f""
    data = {
        "recipient": {"id": recipinet_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send message. Status code:", response.status_code)
