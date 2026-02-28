import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 初始化 Gemini 客戶端
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')

def generate_shopee_content(taobao_content: str, niche: str) -> str:
    """
    將淘寶內文轉換為台灣蝦皮風格的內文
    :param taobao_content: 原始淘寶內文
    :param niche: 商品領域
    """
    system_prompt = f"""
    你是一個台灣蝦皮的超強電商行銷專家，專精於【{niche}】領域。
    請將輸入的「淘寶商品內文」改寫為高轉化率的「台灣蝦皮風格商品詳情」。
    
    嚴格規則：
    1. 翻譯為台灣繁體中文，使用台灣在地慣用語。
    2. 加入「台灣在地服務」的保證（例如：出貨前檢查、七天鑑賞期等）。
    3. 內容排版清晰，善用條列式與 Emoji 增加易讀性。
    4. 強化「買家心理訴求」（如：CP值高、回購率強、新手好上手等字眼）。
    5. 保留原有技術規格數字，並用粗體強調。
    """

    try:
        response = model.generate_content(
            f"{system_prompt}\n\n請改寫這個淘寶商品內文：\n{taobao_content}"
        )
        return response.text.strip()
    except Exception as e:
        return f"發生錯誤: {e}"

if __name__ == "__main__":
    test_content = "此款机架采用3K纯碳纤维打造，重量仅65g，支持安装20x20mm飞控塔。抗摔性极强，适合新手练习炸机。配件清单包括底板、顶板和机臂。"
    print("【原內文】:\n", test_content)
    print("\n【蝦皮版】:\n", generate_shopee_content(test_content, niche="無人機 DIY"))
