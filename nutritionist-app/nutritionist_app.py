#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App - 食物圖片識別 + 營養分析
使用 Hugging Face API + LLM 營養建議
"""

import urllib.request
import urllib.error
import json
import base64
import os
import sys
from datetime import datetime

# ============ 配置 ============
HF_TOKEN = os.environ.get("HF_API_KEY", "")
MODEL_ID = "google/siglip-so400m-patch14-384"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"

# Aliyun API (用於營養分析)
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "")
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# ============ 食物識別 ============
def recognize_food(image_path):
    """識別食物圖片"""
    print("\n🔍 識別食物...")
    
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except Exception as e:
        return {"error": f"圖片載入失敗：{e}"}
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    
    try:
        req = urllib.request.Request(
            HF_API_URL,
            data=image_data,
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        if isinstance(result, list):
            labels = [item.get("label", "") for item in result[:5]]
            return {"food_items": labels, "raw": result}
        else:
            return {"food_items": [str(result)], "raw": result}
            
    except Exception as e:
        return {"error": f"API 調用失敗：{e}"}

# ============ 營養分析 ============
def analyze_nutrition(food_items):
    """分析食物營養成分"""
    print("\n📊 分析營養成分...")
    
    foods_str = ", ".join(food_items)
    
    prompt = f"""請分析以下食物的營養成分：{foods_str}

請以 JSON 格式返回營養信息。"""

    headers = {
        "Authorization": f"Bearer {ALIYUN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen3.5-plus",
        "messages": [
            {"role": "system", "content": "你是一位專業營養師。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        req = urllib.request.Request(
            ALIYUN_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        return {"nutrition_analysis": content}
            
    except Exception as e:
        return {"error": f"營養分析失敗：{e}"}

# ============ 主函數 ============
def main():
    """主函數"""
    print("=" * 60)
    print("🥗 營養師 App - 食物圖片識別 + 營養分析")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法：python3 nutritionist_app.py <圖片路徑>")
        return 1
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"\n❌ 錯誤：找不到圖片 '{image_path}'")
        return 1
    
    # 1. 識別食物
    recognition_result = recognize_food(image_path)
    
    if "error" in recognition_result:
        print(f"\n❌ {recognition_result['error']}")
        return 1
    
    food_items = recognition_result.get("food_items", [])
    
    if not food_items:
        print("\n❌ 無法識別食物")
        return 1
    
    print(f"\n✅ 識別到：{', '.join(food_items)}")
    
    # 2. 營養分析
    nutrition_data = analyze_nutrition(food_items)
    
    if "error" in nutrition_data:
        print(f"\n⚠️ {nutrition_data['error']}")
    
    print("\n✅ 分析完成！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
