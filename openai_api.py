import requests
from config import OPENROUTER_API_KEY, ZALO_OA_LINK, HOTLINE
from fb_graph_api import send_text_message, send_button_message

def ask_openai(prompt: str, sender_id: str = None) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "Bạn là một nhân viên tư vấn tận tâm và thân thiện của Tập đoàn Cung ứng Nhân lực Sao Mai, "
        "chuyên tư vấn xuất khẩu lao động và du học Đài Loan, Nhật Bản, Hàn Quốc.\n\n"
        "Luôn trả lời khách bằng văn phong tự nhiên, gần gũi, xưng hô 'em – anh/chị'. "
        "Không dùng các câu máy móc như 'Tôi rất vui được hỏi của bạn'. Tuyệt đối không ký tên.\n\n"
        "Cấu trúc trả lời:\n"
        "- Mở đầu: 'Em chào anh/chị ạ! Cảm ơn anh/chị đã nhắn tin cho Tập đoàn Cung ứng Nhân lực Sao Mai.'\n"
        "- Nội dung: Trả lời rõ ràng đúng câu hỏi, có thể dùng emoji nếu cần\n"
        f"- Kết thúc: 'Anh/chị có thể nhắn thêm cho em nếu cần hỗ trợ nha. 👉 Nhấn vào đây: {ZALO_OA_LINK} hoặc gọi {HOTLINE} để gặp nhân viên tư vấn ạ! ❤️'\n"
    )

    data = {
        "model": "mistralai/mistral-small",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            content = result["choices"][0]["message"]["content"].strip()

            # ✅ Fix văn phong máy móc nếu có
            if "Tôi rất vui được hỏi của bạn" in content or (
                "Xin chào" in content and "Tôi rất vui" in content
            ):
                content = (
                    "Em chào anh/chị ạ! Cảm ơn anh/chị đã nhắn tin cho Tập đoàn Cung ứng Nhân lực Sao Mai.\n\n"
                    "Chi phí và mức lương khi đi Đài Loan có thể dao động tùy vào ngành nghề, kinh nghiệm và đơn hàng cụ thể ạ. "
                    "Thông thường, chi phí xuất cảnh trọn gói khoảng 20–30 triệu VNĐ, thu nhập trung bình từ 18–25 triệu/tháng.\n\n"
                    f"Anh/chị có thể nhắn thêm cho em nếu cần hỗ trợ nha. 👉 Nhấn vào đây: {ZALO_OA_LINK} hoặc gọi {HOTLINE} để gặp nhân viên tư vấn ạ! ❤️"
                )

            # 👉 Gửi kết quả về Messenger nếu có sender_id
            if sender_id:
                send_text_message(sender_id, content)

                # Gửi thêm nút liên hệ nếu muốn
                send_button_message(
                    recipient_id=sender_id,
                    text="👉 Anh/chị có thể chọn cách liên hệ nhanh nhất ạ:",
                    zalo_url=ZALO_OA_LINK,
                    hotline=HOTLINE
                )

            return content

        else:
            print(f"🤖 OpenRouter full response: {result}")
            error_msg = result.get("error", {}).get("message", "Lỗi không xác định.")
            if sender_id:
                send_text_message(sender_id, f"[❌ GPT ERROR] {error_msg}")
            return "[❌ GPT ERROR] " + error_msg

    except Exception as e:
        print(f"❌ Exception: {e}")
        if sender_id:
            send_text_message(sender_id, "[❌ GPT ERROR] Không kết nối được OpenRouter API.")
        return "[❌ GPT ERROR] Không kết nối được OpenRouter API."
