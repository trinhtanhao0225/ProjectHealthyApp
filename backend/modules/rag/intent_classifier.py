def classify_intent(query):
    """Phân loại truy vấn của người dùng thành các chủ đề chính."""
    query_lower = query.lower()
    
    # 1. Kế hoạch ăn uống/Chế độ (Độ ưu tiên cao nhất)
    keywords_plan = ["kế hoạch", "thực đơn", "chế độ", "ăn kiêng", "cân bằng", "trong ngày", "cho bữa"]
    if any(k in query_lower for k in keywords_plan):
        return "PLANNING"
        
    # 2. Sức khỏe/Tư vấn/Bệnh lý
    keywords_health = ["sức khỏe", "bệnh", "tư vấn", "ăn uống", "tăng cân", "giảm cân", "dị ứng", "huyết áp", "tiểu đường", "thận", "ung thư"]
    if any(k in query_lower for k in keywords_health):
        return "HEALTH_ADVICE"

    # 3. Dinh dưỡng/Thông tin thực phẩm cụ thể
    keywords_nutrient = ["dinh dưỡng", "calo", "protein", "chất béo", "có bao nhiêu", "vitamin", "khoáng chất", "chứa"]
    if any(k in query_lower for k in keywords_nutrient):
        return "FOOD_INFO"

    # 4. Truy vấn chung không liên quan đến dinh dưỡng
    if len(query.split()) < 3 and ("là gì" in query_lower or "ai là" in query_lower):
        return "GENERAL_OTHER" # Ví dụ: "Thủ đô Việt Nam là gì?"

    # Mặc định là tìm kiếm thực phẩm và đưa ra tóm tắt
    return "SEARCH_SUMMARY" 