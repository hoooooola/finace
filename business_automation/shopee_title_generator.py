import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 初始化 Gemini 客戶端
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 設定模型 (使用 gemini-2.5-flash 作為快速且便宜的文字處理預設值，若環境支援可替換對應模型)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_shopee_title(taobao_title: str, niche: str) -> str:
    """
    將淘寶標題轉換為台灣蝦皮風格的標題
    :param taobao_title: 原始淘寶標題
    :param niche: 商品領域 (例如：無人機 DIY、戶外裝備)
    """
    system_prompt = f"""
    你是一個台灣蝦皮的超強電商行銷專家，專精於【{niche}】領域。
    請將輸入的「淘寶商品標題」改寫為高點擊率的「台灣蝦皮風格標題」。
    
    嚴格規則：
    1. 翻譯為台灣繁體中文，使用台灣在地慣用語（如：攝像頭->鏡頭，性價比->高CP值，質量->品質，內存->記憶體）。
    2. 標題開頭加上強而有力的促銷標籤（例如：【台灣現貨】、【免運優惠】或【24H出貨】）。
    3. 加入 1~2 個適當的 Emoji（如 🚀、🔥、✨）增加視覺吸睛度，但不要過多。
    4. 突顯該領域受眾最在意的賣點（規格清晰、新手友善、耐用等）。
    5. 字數請務必控制在蝦皮標題限制的 60 個字元（繁體中文）以內，不要廢話。
    """

    try:
        response = model.generate_content(
            f"{system_prompt}\n\n請改寫這個淘寶標題：\n{taobao_title}"
        )
        return response.text.strip()
    except Exception as e:
        return f"發生錯誤: {e}"

if __name__ == "__main__":
    test_title = "新款大疆无人机配件 FPV穿越机机架 碳纤维机身 耐摔耐撞 航模配件 质量好性价比高"
    print("【原標題】:", test_title)
    print("【蝦皮版】:", generate_shopee_title(test_title, niche="無人機 DIY"))
