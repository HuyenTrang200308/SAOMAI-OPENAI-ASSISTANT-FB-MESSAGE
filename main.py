import time
import threading
from datetime import datetime
from utils import is_office_hours, load_keywords, match_intent, log_message
from fb_graph_api import send_text_message, send_quick_reply, send_button_message
from openai_api import ask_openai
from config import ZALO_OA_LINK, HOTLINE, REPLY_TIMEOUT_SECONDS

# Load từ khóa
KEYWORDS = load_keywords()

# Theo dõi người dùng
greeted_users = set()
pending_users = {}
user_last_message_time = {}

# Tránh phản hồi lặp lại
recent_users = {}
REPLY_COOLDOWN = 5  # thời gian chờ giữa 2 lần phản hồi

# -------------------------------
# XỬ LÝ TIN NHẮN KHÁCH GỬI
# -------------------------------
def handle_message(sender_id: str, message_text: str, quick_reply_payload: str = None):
    log_message(sender_id, message_text)
    now = time.time()
    last_time = recent_users.get(sender_id, 0)

    if now - last_time < REPLY_COOLDOWN:
        print(f"⏳ Gửi gần đây → bỏ qua")
        return

    recent_users[sender_id] = now
    user_last_message_time[sender_id] = now
    is_office = is_office_hours()

    if quick_reply_payload:
        handle_quick_reply(sender_id, quick_reply_payload)
        return

    # 1. Thử tìm intent từ từ khóa

    if sender_id not in greeted_users:
        greeted_users.add(sender_id)
        if is_office:
            send_text_message(sender_id,
                "🌟 Em chào anh/chị ạ! Cảm ơn anh/chị đã nhắn tin cho Tập đoàn Cung ứng Nhân lực Sao Mai.\n"
                "Hiện tại anh/chị đang nhắn tin *trong giờ làm việc*, em đã báo cho bộ phận tư vấn rồi, các bạn sẽ phản hồi lại anh/chị sớm nhất có thể ạ. Mình vui lòng đợi chút nha! 😊"
            )
        else:
            send_text_message(sender_id,
                "🌟 Em chào anh/chị ạ! Cảm ơn anh/chị đã liên hệ với Tập đoàn Cung ứng Nhân lực Sao Mai.\n"
                "Hiện tại là *ngoài giờ làm việc* (8h–17h, Thứ 2–Thứ 6) nên chưa có nhân viên trực tiếp hỗ trợ.\n"
                "Nhưng không sao, em là *trợ lý ảo của Sao Mai*, em sẽ hỗ trợ anh/chị ngay bây giờ ạ!"
            )
            send_quick_reply(
                sender_id,
                "👉 Anh/chị đang quan tâm đến chương trình nào dưới đây ạ?",
                ["XKLĐ Nhật Bản 🇯🇵", "XKLĐ Đài Loan 🇹🇼", "Du học Hàn – Nhật – Đài 🎓", "Kết nối Zalo 💬"]
            )
            return

    if is_office:
        handle_during_working_hours(sender_id, now)
        
    intent = match_intent(message_text, KEYWORDS)

    # 2. Nếu có intent → dùng OpenAI xử lý theo nội dung người dùng hỏi
    if intent:
        ask_openai(message_text, sender_id)
        return

    # 3. Nếu không có intent → vẫn dùng OpenAI để trả lời tự nhiên
    ask_openai(message_text, sender_id)
    return

# -------------------------------
# TRONG GIỜ HÀNH CHÍNH: CHỜ 5 PHÚT
# -------------------------------
def handle_during_working_hours(sender_id: str, message_time: float):
    send_text_message(sender_id,
        "🕒 Hiện tại anh/chị đang nhắn *trong giờ làm việc*.\n"
        "Nhân viên tư vấn của Sao Mai sẽ phản hồi anh/chị trong ít phút tới. Anh/chị vui lòng đợi nhé! 😊"
    )

    if sender_id in pending_users:
        return

    def wait_and_handle():
        time.sleep(REPLY_TIMEOUT_SECONDS)
        if user_last_message_time.get(sender_id, 0) > message_time:
            return

        send_text_message(sender_id,
            "🤖 Dạ hiện tại nhân viên tư vấn bên em chưa kịp phản hồi ạ.\n"
            "Em là *trợ lý ảo của Tập đoàn Cung ứng Nhân lực Sao Mai*, xin phép được hỗ trợ anh/chị trước nhé!"
        )
        send_quick_reply(
            sender_id,
            "👉 Anh/chị đang quan tâm đến chương trình nào ạ?",
            ["XKLĐ Nhật Bản 🇯🇵", "XKLĐ Đài Loan 🇹🇼", "Du học Hàn – Nhật – Đài 🎓", "Kết nối Zalo 💬"]
        )

    pending_users[sender_id] = True
    threading.Thread(target=wait_and_handle).start()

# -------------------------------
# QUICK REPLY
# -------------------------------
def handle_quick_reply(sender_id: str, payload: str):
    if payload == "XKLĐ Nhật Bản 🇯🇵":
        send_text_message(sender_id,
            "🇯🇵 *Chương trình Xuất khẩu lao động Nhật Bản* đang được rất nhiều bạn quan tâm với thu nhập từ *26–35 triệu/tháng*.\n"
            "✅ Chi phí minh bạch, đơn hàng liên tục, đào tạo bài bản.\n"
            "Anh/chị muốn biết thêm về phần nào ạ?"
        )
        send_quick_reply(
            sender_id,
            "👉 Em có thể hỗ trợ thêm thông tin gì cho mình ạ?",
            ["Chi phí đi Nhật", "Hồ sơ đi Nhật", "Quy trình đi Nhật"]
        )

    elif payload == "XKLĐ Đài Loan 🇹🇼":
        send_text_message(sender_id,
            "🇹🇼 *XKLĐ Đài Loan* nổi bật với chi phí thấp, xuất cảnh nhanh và thu nhập ổn định từ *18–25 triệu/tháng*.\n"
            "Anh/chị muốn tìm hiểu thêm về phần nào ạ?"
        )
        send_quick_reply(
            sender_id,
            "👉 Em có thể hỗ trợ thêm thông tin gì cho mình ạ?",
            ["Chi phí đi Đài Loan", "Hồ sơ đi Đài Loan", "Thời gian xuất cảnh"]
        )

    elif payload == "Du học Hàn – Nhật – Đài 🎓":
        send_text_message(sender_id,
            "🎓 *Du học vừa học vừa làm* là lựa chọn được nhiều bạn trẻ theo đuổi hiện nay.\n"
            "Chi phí hợp lý – Có cơ hội làm thêm – Bằng cấp quốc tế.\n"
            "Anh/chị quan tâm điều gì nhất ạ?"
        )
        send_quick_reply(
            sender_id,
            "👉 Em có thể hỗ trợ thêm thông tin nào ạ?",
            ["Điều kiện du học", "Học phí", "Ngành học phổ biến"]
        )

    elif payload == "Kết nối Zalo 💬":
        send_button_message(
            recipient_id=sender_id,
            text="👉 Anh/chị có thể chọn 1 trong các cách sau để được hỗ trợ nhanh nhất ạ:",
            zalo_url=ZALO_OA_LINK,
            hotline=HOTLINE,
            extra_button={
                "type": "web_url",
                "url": "https://saomaixkld.vn/",
                "title": "📋 Xem đơn hàng"
            }
        )

    else:
        # ✅ Các từ khóa như: "Chi phí đi Nhật", "Thời gian xuất cảnh", v.v...
        ask_openai(payload, sender_id)
