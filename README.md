# 🤖 SAO MAI - OpenAI Assistant Facebook Messenger Chatbot

Chatbot AI tự động phản hồi tin nhắn khách hàng trên Facebook Page ngoài giờ hành chính.  
Dự án được phát triển bởi Tập đoàn Cung ứng Nhân lực Sao Mai.

---

## 🚀 Tính năng chính

- 🕒 Phân biệt thời gian làm việc:
  - Trong giờ hành chính (8h–17h, Thứ 2–Thứ 6): **không tự động trả lời**
  - Ngoài giờ hành chính: **chatbot AI hoạt động tự động**
- 🤖 Trả lời tự nhiên như người thật
- 🧠 Xử lý linh hoạt bằng từ khóa (dùng `keywords.json`)
- 💬 Gợi ý Quick Reply (XKLD Nhật, Đài, Du học...)
- 🔗 Điều hướng khách hàng sang Zalo OA: [Zalo.me/123456789](https://zalo.me/saomaihr0931446688)

---

## 🛠️ Công nghệ sử dụng

- Python + Flask
- Facebook Graph API (Messenger Webhook)
- OpenAI API (GPT Assistant)
- Tệp từ khóa tùy biến (`keywords.json`)

---

## ⚙️ Cài đặt & chạy local

```bash
# 1. Clone repo
git clone https://github.com/HuyenTrang200308/SAOMAI-OPENAI-ASSISTANT-FB-MESSAGE.git
cd SAOMAI-OPENAI-ASSISTANT-FB-MESSAGE

# 2. Cài thư viện cần thiết
pip install -r requirements.txt

# 3. Tạo file .env từ .env.example và thêm các token cần thiết
cp .env.example .env  # hoặc tạo thủ công

# 4. Chạy Flask app
python run.py
