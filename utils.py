import json
from datetime import datetime
from config import WORK_HOUR_START, WORK_HOUR_END, WORK_DAYS
from typing import Optional

from datetime import datetime

def is_office_hours():
    # now = datetime.now()
    # hour = now.hour
    # minute = now.minute
    # weekday = now.weekday()  # Thứ 2 = 0, Chủ nhật = 6

    # Nếu là thứ 7 hoặc Chủ nhật → không phải giờ hành chính
    # if weekday >= 5:
       # return False

    # Giờ hành chính: 8h–12h và 13h–17h
    # if 8 <= hour < 12:
        # return True
    # if 13 <= hour < 17:
        # return True

    # Giờ nghỉ trưa hoặc ngoài giờ → không tính là giờ hành chính
    return False


def load_keywords(filepath: str = "keywords.json") -> dict:
    """Đọc file keywords.json và trả về dạng dict"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def match_intent(message: str, keywords: dict) -> Optional[str]:
    """
    So khớp nội dung tin nhắn với các từ khóa.
    Trả về tên nhóm nếu khớp, hoặc None nếu không khớp.
    """
    message = message.lower()
    for intent, samples in keywords.items():
        for sample in samples:
            if sample in message:
                return intent
    return None

def format_time(dt: Optional[datetime] = None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%H:%M:%S %d-%m-%Y")

def log_message(sender_id: str, message_text: str):
    now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    print(f"[{now}] 💬 {sender_id}: {message_text}")

