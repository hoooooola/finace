import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"請改寫這個淘寶標題：\n{taobao_title}"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"發生錯誤: {e}"

if __name__ == "__main__":
    test_title = "新款大疆无人机配件 FPV穿越机机架 碳纤维机身 耐摔耐撞 航模配件 质量好性价比高"
    print("【原標題】:", test_title)
    print("【蝦皮版】:", generate_shopee_title(test_title, niche="無人機 DIY"))
