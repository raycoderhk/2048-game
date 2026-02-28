#!/usr/bin/env python3
"""
食物識別 + 營養分析（混合方案）
- 圖片識別：Hugging Face 免費 API / 本地模型
- 營養分析：阿里雲 Coding Plan (¥39.9/月 包月)

無需額外開通阿里雲百煉！
"""

import urllib.request
import urllib.error
import json
import base64
import sys
import os

# 配置
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY")
ALIYUN_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

# Hugging Face API (免費，無需 API Key)
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

def recognize_food_with_hf(image_path: str):
    """
    方法 1: 用 Hugging Face 免費 API 識別食物
    免費額度：約 1000 次/月
    """
    print("\n🔍 方法 1: Hugging Face 免費 API")
    print("=" * 60)
    
    try:
        # 讀取圖片
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Hugging Face Inference API
        payload = {
            "inputs": image_data.decode("latin-1")
        }
        
        req = urllib.request.Request(
            HF_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        # 解析結果
        if isinstance(result, list) and len(result) > 0:
            caption = result[0].get("generated_text", "未知食物")
            print(f"✅ 識別結果：{caption}")
            return caption
        else:
            print(f"⚠️  無法識別，返回：{result}")
            return None
            
    except urllib.error.HTTPError as e:
        print(f"⚠️  Hugging Face API 錯誤：{e.code}")
        print(f"   可能原因：速率限制 / 模型載入中")
        return None
    except Exception as e:
        print(f"⚠️  錯誤：{e}")
        return None

def analyze_nutrition_with_aliyun(food_name: str):
    """
    用阿里雲 Coding Plan 分析營養成份
    """
    print("\n📊 使用阿里雲 Coding Plan 分析營養")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {ALIYUN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen-plus",
        "messages": [
            {
                "role": "system",
                "content": "你係一個專業營養師。請提供準確、實用嘅營養資訊。"
            },
            {
                "role": "user",
                "content": f"請分析「{food_name}」嘅營養成份，包括：卡路里、蛋白質、脂肪、碳水化合物、纖維、鈉。請用表格形式，並提供每 100 克同埋一般份量嘅數據。"
            }
        ]
    }
    
    url = f"{ALIYUN_BASE_URL}/chat/completions"
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            
            print("✅ 營養分析成功！")
            print("\n📊 營養成份：")
            print("-" * 60)
            print(answer)
            print("-" * 60)
            
            if "usage" in result:
                usage = result["usage"]
                print(f"\n💰 Token 使用量：{usage.get('total_tokens', 'N/A')} tokens")
                print(f"   (包喺 ¥39.9/月 內，唔使額外付費！)")
            
            return answer
        else:
            print(f"❌ API 回應異常：{result}")
            return None
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP 錯誤：{e.code}")
        print(f"   錯誤：{e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
        return None

def recognize_food_with_description(image_path: str):
    """
    方法 2: 如果 Hugging Face 失敗，讓用戶手動輸入
    """
    print("\n📝 方法 2: 手動輸入食物名稱")
    print("=" * 60)
    
    food_name = input("請輸入食物名稱（例如：麥片、炒飯、沙律）：")
    return food_name.strip()

def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("🍎 食物營養分析（混合方案）")
    print("=" * 60)
    print("圖片識別：Hugging Face (免費)")
    print("營養分析：阿里雲 Coding Plan (¥39.9/月 包月)")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n❌ 請提供圖片路徑！")
        print("   用法：python3 food_recognition_hybrid.py <圖片路徑>")
        return
    
    image_path = sys.argv[1]
    
    # 步驟 1: 識別食物
    print("\n📸 圖片路徑：{image_path}")
    print("\n正在識別食物...")
    
    food_name = recognize_food_with_hf(image_path)
    
    if not food_name:
        print("\n⚠️  自動識別失敗，請手動輸入。")
        food_name = recognize_food_with_description(image_path)
    
    # 步驟 2: 分析營養
    print(f"\n🔍 準備分析：{food_name}")
    nutrition_data = analyze_nutrition_with_aliyun(food_name)
    
    if nutrition_data:
        print("\n" + "=" * 60)
        print("✅ 分析完成！")
        print("=" * 60)
        print(f"📸 圖片：{image_path}")
        print(f"🍽️  食物：{food_name}")
        print(f"💰 成本：¥0 (包喺 Coding Plan 內！)")
        print("=" * 60)
    else:
        print("\n❌ 分析失敗，請稍後再試。")

if __name__ == "__main__":
    main()
