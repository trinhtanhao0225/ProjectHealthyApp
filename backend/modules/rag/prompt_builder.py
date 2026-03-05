# app/modules/rag/prompt_builder.py
import json
from backend.utils.logger import log

def fallback_summary(prepped_items, query, max_items=6):
    items = prepped_items[:max_items] if prepped_items else []
    if not items:
        return f"Không tìm thấy món ăn nào cho \"{query}\". Vui lòng thử lại với từ khóa khác."
    names = [it["name"] for it in items]
    s = f"Tìm thấy {len(prepped_items)} món ăn cho \"{query}\". Một số lựa chọn: {', '.join(names[:5])}."
    if items and items[0].get("nutrients"):
        s += "\nVí dụ dinh dưỡng: "
        for it in items[:3]:
            top_n = ", ".join(list(it["nutrients"].keys())[:2])
            s += f"{it['name']} (chứa {top_n}); "
    s += "\nHãy cho tôi biết nếu bạn muốn kế hoạch ăn uống chi tiết!"
    return s

# Các hàm prompt dài (copy nguyên từ code của bạn)
def build_summary_prompt(prepped_items, query, max_items_in_prompt=8, user_info=None):
    items_json = json.dumps(prepped_items[:max_items_in_prompt], ensure_ascii=False, indent=2) if prepped_items else "[]"
    user_str = f"Thông tin người dùng: {json.dumps(user_info, ensure_ascii=False, indent=2)}\n\n" if user_info else ""
    
    return f"""Bạn là một trợ lý ẩm thực và dinh dưỡng, chuyên gia về sức khỏe cá nhân. {user_str}
Dưới đây là dữ liệu JSON gồm các thực phẩm/nguyên liệu (mỗi phần tử có fdcId, name, description, nutrients, ingredients).

JSON_DANH_SACH:
{items_json}

Yêu cầu:
1) Viết một câu trả lời bằng TIẾNG VIỆT, thân thiện và dễ hiểu cho người dùng.
2) Bắt đầu bằng một tóm tắt ngắn (1-2 câu) nêu tổng quan những lựa chọn phù hợp với truy vấn: "{query}".
3) Dựa trên DỮ LIỆU CÁ NHÂN (dị ứng, bệnh, mục tiêu) và DỮ LIỆU THỰC PHẨM (JSON) để đưa ra lời khuyên an toàn và cá nhân hóa.
4) Gợi ý 2-4 cách sử dụng hoặc món ăn/kế hoạch ăn nhanh có thể làm từ các thực phẩm này.
5) Kết thúc bằng một câu hỏi ngắn khuyến khích người dùng hỏi chi tiết hơn.
Lưu ý: KHÔNG lặp lại nguyên văn JSON. Ưu tiên độ an toàn và sự phù hợp dinh dưỡng."""

def generate_health_advice_prompt(prepped_items, query, user_info):
    items_json = json.dumps(prepped_items, ensure_ascii=False, indent=2)
    
    # Format user info rõ ràng hơn
    user_details = ""
    if user_info:
        user_details = f"""
📋 THÔNG TIN SỨC KHỎE NGƯỜI DÙNG:
- Họ tên: {user_info.get('name', 'N/A')}
- Tuổi: {user_info.get('age', 'N/A')} tuổi
- Giới tính: {user_info.get('gender', 'N/A')}
- Chiều cao: {user_info.get('height', 'N/A')} cm
- Cân nặng hiện tại: {user_info.get('weight', 'N/A')} kg
- Cân nặng mục tiêu: {user_info.get('targetWeight', 'N/A')} kg
- Mục tiêu: {user_info.get('target', 'N/A')} (Giảm cân/Tăng cân/Duy trì)
- Mức độ vận động: {user_info.get('exercise', 'N/A')}
- BMR (Chuyển hóa cơ bản): {user_info.get('bmr', 'N/A')} kcal/ngày
- TDEE (Tiêu hao năng lượng): {user_info.get('tdee', 'N/A')} kcal/ngày
- Dị ứng: {', '.join(user_info.get('allergies', [])) if user_info.get('allergies') else 'Không'}
- Bệnh nền: {', '.join(user_info.get('diseases', [])) if user_info.get('diseases') else 'Không'}
- Ghi chú: {user_info.get('note', 'Không có')}
"""
    
    return f"""Bạn là một Chuyên gia Dinh dưỡng và Sức khỏe cá nhân người Việt Nam. 
Hãy tư vấn ngắn gọn, chính xác và hữu ích cho yêu cầu: "{query}"

{user_details}

DANH SÁCH THỰC PHẨM TÌM KIẾM ĐƯỢC (nếu liên quan):
{items_json}

═══════════════════════════════════════════════════════════════════════

HỆ THỐNG TƯ VẤN:

1️⃣ PHÂN TÍCH SỨC KHỎE CÁ NHÂN:
   - Tóm tắt tình trạng sức khỏe hiện tại DỰA TRÊN DỮ LIỆU (Tuổi, Cân nặng, BMR, TDEE, Mục tiêu).
   - Xác định nhu cầu dinh dưỡng cụ thể cho người dùng này.

2️⃣ CẢNH BÁO AN TOÀN (ĐẠO HAM QUAN TRỌNG):
   - Kiểm tra NGAY LẬP TỨC nếu có BẤT KỲ XUNG ĐỘT nào giữa:
     * Danh sách DỊ ỨNG của người dùng
     * Danh sách BỆNH LÝ của người dùng
     * Các thực phẩm trong danh sách JSON
   - Nếu phát hiện xung đột → CẢNh báo RÕNG RÀNG với màu đỏ tâm lý (ví dụ: "⚠️ CẢNH BÁO: Nếu bạn dị ứng lạc, hạn chế/tránh các sản phẩm có chứa lạc").
   - Nếu người dùng có bệnh Thận → Giải thích cần hạn chế Kali, Sodium, Protein cao.
   - Nếu người dùng có bệnh Tim → Hạn chế muối, chất béo bão hòa.
   - Nếu người dùng có Tiểu đường → Hạn chế đường, chọn carb phức tạp.

3️⃣ LỜI KHUYÊN DINH DƯỠNG TỪ THỰC PHẨM CÓ SẴN:
   - Dựa vào DANH SÁCH THỰC PHẨM JSON: gợi ý 2-3 cách sử dụng hoặc món ăn an toàn.
   - Gợi ý cách chế biến phù hợp với bệnh lý (nếu có).
   - Ưu tiên thực phẩm giàu vitamin, khoáng chất phù hợp với tình trạng sức khỏe.

4️⃣ TÍNH TOÁN CALO VÀ DINH DƯỠNG (nếu có TDEE):
   - Nếu mục tiêu là GIẢM CÂN: Gợi ý lượng calo cần thiết ≈ TDEE - 300-500 kcal
   - Nếu mục tiêu là TĂNG CÂN: Gợi ý lượng calo cần thiết ≈ TDEE + 300-500 kcal
   - Nếu mục tiêu là DUY TRÌ: Lượng calo ≈ TDEE

═══════════════════════════════════════════════════════════════════════

🎯 ĐỊNH DẠNG CÂU TRẢ LỜI:
- Viết hoàn toàn bằng TIẾNG VIỆT, thân thiện, dễ hiểu.
- Sử dụng emoji để dễ theo dõi.
- Ưu tiên TUYỆT ĐỐI sự an toàn (Dị ứng & Bệnh lý).
- KHÔNG lặp lại nguyên văn JSON trong trả lời.
- Kết thúc bằng câu hỏi khuyến khích hỏi thêm chi tiết.

LƯU Ý QUAN TRỌNG:
- Nếu không có thông tin nào trong JSON → Hãy dùng kiến thức chung để tư vấn.
- TUYỆT ĐỐI không đưa ra lời khuyên y tế ngoài sức khỏe định mức (ví dụ: không chữa bệnh).
- Luôn ưu tiên sự an toàn hơn là lợi suất dinh dưỡng.
"""

def generate_detailed_planning_prompt(prepped_items, query, user_info):
    items_json = json.dumps(prepped_items, ensure_ascii=False, indent=2)
    
    # Format user info rõ ràng hơn
    user_details = ""
    if user_info:
        user_details = f"""
📋 THÔNG TIN SỨC KHỎE NGƯỜI DÙNG:
- Họ tên: {user_info.get('name', 'N/A')}
- Tuổi: {user_info.get('age', 'N/A')} tuổi
- Giới tính: {user_info.get('gender', 'N/A')}
- Chiều cao: {user_info.get('height', 'N/A')} cm
- Cân nặng hiện tại: {user_info.get('weight', 'N/A')} kg
- Cân nặng mục tiêu: {user_info.get('targetWeight', 'N/A')} kg
- Mục tiêu: {user_info.get('target', 'N/A')} (Giảm cân/Tăng cân/Duy trì)
- Mức độ vận động: {user_info.get('exercise', 'N/A')}
- BMR (Chuyển hóa cơ bản): {user_info.get('bmr', 'N/A')} kcal/ngày
- TDEE (Tiêu hao năng lượng): {user_info.get('tdee', 'N/A')} kcal/ngày
- Dị ứng: {', '.join(user_info.get('allergies', [])) if user_info.get('allergies') else 'Không'}
- Bệnh nền: {', '.join(user_info.get('diseases', [])) if user_info.get('diseases') else 'Không'}
- Ghi chú: {user_info.get('note', 'Không có')}
"""

    return f"""🎯 Bạn là Chuyên gia Dinh dưỡng Cá nhân (AI Nutritionist). 
Nhiệm vụ: LẬP KẾ HOẠCH ĂN UỐNG CHI TIẾT dựa trên dữ liệu người dùng cụ thể và danh sách thực phẩm gợi ý.
Truy vấn: "{query}"

═══════════════════════════════════════════════════════════════════════

1️⃣ THÔNG TIN NGƯỜI DÙNG:
{user_details}

2️⃣ DANH SÁCH THỰC PHẨM CÓ SẴN (Tham khảo để xây dựng kế hoạch):
{items_json}

═══════════════════════════════════════════════════════════════════════

3️⃣ QUY TRÌNH PHÂN TÍCH (STEP-BY-STEP):

📊 BƯỚC 1 - TÍNH TOÁN NHU CẦU:
   - Tính BMI: weight / (height^2 / 10000) = ?
   - Phân loại tình trạng (Thiếu cân/Bình thường/Thừa cân/Béo phì)
   - Nhu cầu calo HÀNG NGÀY dựa trên MỤC TIÊU:
     * Nếu GIẢM CÂN: Calo = TDEE - 300-500 kcal
     * Nếu TĂNG CÂN: Calo = TDEE + 300-500 kcal
     * Nếu DUY TRÌ: Calo = TDEE

🚨 BƯỚC 2 - KIỂM TRA AN TOÀN (TUYỆT ĐỐI QUAN TRỌNG):
   - ✗ LOẠI BỎ NGAY LẬP TỨC: Bất kỳ thực phẩm nào TRÙng với DỊ ỨNG.
   - ✗ CẬM GIẢM: Thực phẩm không phù hợp với BỆNH LÝ.
     * Bệnh Thận → Hạn chế Kali, Sodium, Protein cao
     * Bệnh Tim → Hạn chế Sodium, chất béo bão hòa
     * Tiểu đường → Hạn chế đường đơn giản, ưu tiên glycemic index thấp
     * Cao huyết áp → Hạn chế Sodium, ưu tiên K+, Mg+
   - Nếu phát hiện xung đột → DỪNG NGAY và BÁO CÁO cho người dùng.

✅ BƯỚC 3 - XÂY DỰNG THỰC ĐƠN:
   - Lựa chọn thực phẩm từ JSON SAU KHI LOẠI BỎ những cái không an toàn.
   - Xây dựng thực đơn CÂN BẰNG 3-4 bữa/ngày (Sáng, Trưa, Chiều/Xen, Tối).
   - Mỗi bữa cần bao gồm: Protein, Carb, Chất béo, Vitamin & Khoáng chất.
   - Tính toán calo GẦN ĐÚNG cho mỗi bữa sao cho TỔNG ≈ nhu cầu hàng ngày.

═══════════════════════════════════════════════════════════════════════

4️⃣ ĐỊNH DẠNG CÂU TRẢ LỜI (Trả lời TOÀN TIẾNG VIỆT):

📝 PHẦN 1 - PHÂN TÍCH NHANH
Tóm tắt:
- Tình trạng sức khỏe hiện tại (BMI, mục tiêu)
- Nhu cầu calo hàng ngày (con số cụ thể)
- Khuyến cáo chung (Nếu có bệnh lý, hạn chế gì)
- ⚠️ CẢNH BÁO nếu có xung đột (dị ứng/bệnh)

📝 PHẦN 2 - KẾ HOẠCH CHI TIẾT (3-7 ngày tùy yêu cầu)
Định dạng mỗi bữa:
🍽️ [BUỔI] - [Calo tính toán]
  • Món 1: [Tên] - [Calo/Dinh dưỡng chính] - [Lý do chọn]
  • Món 2: ...
  • Đồ uống: ...

Ví dụ:
🌅 SÁNG (400-450 kcal)
  • Cơm tấm + Trứng chiên: 300 kcal - Giàu protein & carb
  • Rau muống xào: 80 kcal - Giàu sắt, vitamin
  • Nước cam: 50 kcal - Vitamin C

📝 PHẦN 3 - GHI CHÚ GÉP
- Mẹo ăn uống lành mạnh (Cách chế biến, thời gian ăn, v.v.)
- Nước uống khuyến cáo (Nước lạnh, trà xanh, v.v.)
- Lưu ý về kích thước phần ăn
- Gợi ý snack (nếu cần thiết)

═══════════════════════════════════════════════════════════════════════

5️⃣ LƯU Ý QUAN TRỌNG:

✓ Viết hoàn toàn bằng TIẾNG VIỆT.
✓ Sử dụng emoji & Markdown để dễ theo dõi.
✓ TUYỆT ĐỐI kiểm tra Dị ứng & Bệnh lý TRƯỚC khi gợi ý.
✓ Cho con số CALO CỤ THỂ cho mỗi bữa.
✓ KHÔNG lặp lại nguyên văn JSON.
✓ Nếu JSON không đủ thực phẩm → Dùng kiến thức chung để bổ sung nhưng vẫn TUÂN THỦ yêu cầu an toàn.
✓ Kết thúc bằng lời khuyến khích & câu hỏi để tiếp tục tư vấn.

⚠️ TẤT CẢ CHỈ DẨN TRÊN ĐỀU PHẢI TUỲ THEO DỮ LIỆU CÁ NHÂN CỤ THỂ.
"""

def generate_fallback_prompt(prepped_items, query, user_info):
    items_json = json.dumps(prepped_items, ensure_ascii=False, indent=2)
    
    return f"""Bạn là một chuyên gia dinh dưỡng người Việt Nam. Yêu cầu của người dùng: "{query}" không liên quan trực tiếp đến dinh dưỡng hoặc sức khỏe.

THÔNG TIN NGƯỜI DÙNG: {json.dumps(user_info, ensure_ascii=False, indent=2)}

Hãy trả lời bằng Tiếng Việt, thân thiện:

THỪA NHẬN VÀ CHUYỂN HƯỚNG:
Lịch sự giải thích rằng chủ đề không phải lĩnh vực chuyên môn chính của bạn.

ĐỀ XUẤT GIÁN TIẾP:
Nếu có thể liên kết gián tiếp với sức khỏe, gợi ý ngắn gọn (ví dụ: "Nếu bạn hỏi về sức khỏe, tôi có thể tư vấn về chế độ ăn uống").
Hoặc nếu họ muốn tìm thông tin về một thực phẩm cụ thể nào đó, hãy gợi ý hỏi về dinh dưỡng của nó.

KẾT THÚC:
Kết thúc bằng câu hỏi mở để khuyến khích hỏi về dinh dưỡng/sức khỏe cá nhân.

LƯU Ý QUAN TRỌNG:
Trả lời hoàn toàn bằng Tiếng Việt.
Giữ ngắn gọn, tích cực, không vượt quá 200 từ.
"""

# Hàm chọn prompt theo intent
def get_prompt(intent: str, prepped_items, query, user_info=None, max_items_in_prompt=8):
    if intent == "PLANNING":
        return generate_detailed_planning_prompt(prepped_items, query, user_info)
    elif intent in ["HEALTH_ADVICE", "FOOD_INFO"]:
        return generate_health_advice_prompt(prepped_items, query, user_info)
    elif intent == "GENERAL_OTHER":
        return generate_fallback_prompt(prepped_items, query, user_info)
    else:
        return build_summary_prompt(prepped_items, query, max_items_in_prompt, user_info)