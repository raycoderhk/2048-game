#!/usr/bin/env python3
"""
Qwen-VL API 測試腳本
測試阿里雲視覺語言模型是否支援圖片上傳和營養分析
"""

import requests
import base64
import os
from pathlib import Path

# 配置（用你而家嘅 Aliyun API Key）
API_KEY = "sk-sp-8eec812bc72d47c3866d388cef6372f8"  # 你而家用緊嘅 Coding Plan API Key
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

def encode_image_to_base64(image_path: str) -> str:
    """將圖片轉換為 Base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def test_qwen_vl_basic(image_path: str):
    """
    測試 1: 基本圖片識別
    """
    print("\n🧪 測試 1: 基本圖片識別")
    print("=" * 50)
    
    # 將圖片轉為 Base64
    image_base64 = encode_image_to_base64(image_path)
    image_data_uri = f"data:image/jpeg;base64,{image_base64}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen-vl-plus",  # 視覺語言模型
        "messages": [{
            "role": "user",
            "content": [
                {"image": image_data_uri},
                {"text": "這張圖片中有什麼食物？請詳細描述。"}
            ]
        }]
    }
    
    try:
        print(f"📸 正在分析圖片：{image_path}")
        print(f"🤖 使用模型：qwen-vl-plus")
        print("-" * 50)
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            print("✅ API 調用成功！")
            print("\n📝 AI 回答：")
            print(answer)
            
            # 計算 Token 使用量
            usage = result.get("usage", {})
            print(f"\n📊 Token 使用量:")
            print(f"   輸入：{usage.get('input_tokens', 'N/A')} tokens")
            print(f"   輸出：{usage.get('output_tokens', 'N/A')} tokens")
            print(f"   總計：{usage.get('total_tokens', 'N/A')} tokens")
            
            return True
        else:
            print(f"❌ API 調用失敗！")
            print(f"   狀態碼：{response.status_code}")
            print(f"   錯誤訊息：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}")
        return False

def test_qwen_vl_nutrition(image_path: str):
    """
    測試 2: 營養成份分析
    """
    print("\n\n🧪 測試 2: 營養成份分析")
    print("=" * 50)
    
    image_base64 = encode_image_to_base64(image_path)
    image_data_uri = f"data:image/jpeg;base64,{image_base64}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen-vl-plus",
        "messages": [{
            "role": "user",
            "content": [
                {"image": image_data_uri},
                {
                    "text": """請分析這張圖片中的食物，並提供以下營養資訊（盡可能估計）：
1. 食物名稱
2. 估計份量（克或碗/杯等）
3. 卡路里（kcal）
4. 蛋白質（g）
5. 脂肪（g）
6. 碳水化合物（g）
7. 纖維（g）
8. 鈉（mg）

請用表格形式回答。"""
                }
            ]
        }]
    }
    
    try:
        print(f"📸 正在分析營養成份：{image_path}")
        print("-" * 50)
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            print("✅ 營養分析成功！")
            print("\n📊 營養成份表：")
            print(answer)
            
            return True
        else:
            print(f"❌ 營養分析失敗！")
            print(f"   狀態碼：{response.status_code}")
            print(f"   錯誤訊息：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}")
        return False

def test_text_only():
    """
    測試 3: 純文本（驗證你而家嘅 API Key 係咪 work）
    """
    print("\n\n🧪 測試 3: 純文本測試（驗證 API Key）")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen-plus",  # 用你而家用緊嘅文本模型
        "messages": [
            {"role": "system", "content": "你係一個專業營養師。"},
            {"role": "user", "content": "麥片嘅營養成份係咩？"}
        ]
    }
    
    try:
        print("📝 正在測試純文本 API...")
        print("-" * 50)
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            print("✅ 純文本 API 正常！")
            print("\n📝 AI 回答：")
            print(answer)
            
            return True
        else:
            print(f"❌ 純文本 API 失敗！")
            print(f"   狀態碼：{response.status_code}")
            print(f"   錯誤訊息：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}")
        return False

def main():
    """
    主函數
    """
    print("\n" + "=" * 60)
    print("🍎 阿里雲 Qwen-VL API 測試工具")
    print("=" * 60)
    print(f"\n📍 API 端點：{BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:15]}...{API_KEY[-5:]}")
    
    # 測試 3: 純文本（先驗證 API Key 係咪 work）
    text_test_passed = test_text_only()
    
    if not text_test_passed:
        print("\n⚠️  純文本測試失敗！請檢查 API Key 是否正確。")
        print("   你可以到阿里雲控制台查看：https://bailian.console.aliyun.com/")
        return
    
    # 準備測試圖片
    test_images = [
        "test_food.jpg",
        "test_food.png",
        "food.jpg",
        "food.png",
    ]
    
    image_path = None
    for img in test_images:
        if Path(img).exists():
            image_path = img
            break
    
    if not image_path:
        print("\n⚠️  未找到測試圖片！")
        print("   請將一張食物圖片命名為 'test_food.jpg' 並放到同一目錄，然後再運行。")
        print("\n   或者你可以指定圖片路徑：")
        print("   python3 test_qwen_vl.py <圖片路徑>")
        return
    
    # 測試 1: 基本圖片識別
    vl_test_passed = test_qwen_vl_basic(image_path)
    
    if vl_test_passed:
        # 測試 2: 營養成份分析
        test_qwen_vl_nutrition(image_path)
    
    # 總結
    print("\n\n" + "=" * 60)
    print("📊 測試總結")
    print("=" * 60)
    print(f"✅ 純文本 API: {'通過' if text_test_passed else '失敗'}")
    print(f"{'✅' if vl_test_passed else '❌'} Qwen-VL API: {'通過' if vl_test_passed else '失敗'}")
    
    if text_test_passed and vl_test_passed:
        print("\n🎉 恭喜！阿里雲 Qwen-VL API 完全支援圖片上傳！")
        print("   你可以開始開發營養師 App 了！🚀")
    elif text_test_passed and not vl_test_passed:
        print("\n⚠️  純文本 OK，但 Qwen-VL 失敗。")
        print("   可能原因:")
        print("   1. Qwen-VL 模型需要額外開通")
        print("   2. API Key 權限不足")
        print("   3. 需要聯絡阿里雲客服")
    else:
        print("\n❌ 測試失敗，請檢查 API Key 或聯絡阿里雲支援。")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 如果用戶提供了圖片路徑
        image_file = sys.argv[1]
        if Path(image_file).exists():
            # 重命名為 test_food.jpg 以便測試
            import shutil
            shutil.copy(image_file, "test_food.jpg")
            print(f"✅ 已複製圖片：{image_file} -> test_food.jpg")
        else:
            print(f"❌ 找不到圖片：{image_file}")
            sys.exit(1)
    
    main()
