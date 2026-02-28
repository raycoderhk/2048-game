#!/usr/bin/env python3
"""
DeepSeek-VL API 測試
測試 DeepSeek 視覺語言模型是否支援圖片上傳
"""

import urllib.request
import urllib.error
import json
import base64
import sys
import os

# 從環境變數讀取 API Key
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/v1"

if not API_KEY:
    print("❌ 錯誤：找不到環境變數 DEEPSEEK_API_KEY")
    sys.exit(1)

print(f"🔑 使用 DeepSeek API Key: {API_KEY[:15]}...{API_KEY[-5:]}")

def test_deepseek_chat():
    """測試 1: DeepSeek 純文本（驗證 API Key）"""
    print("\n" + "=" * 60)
    print("🧪 測試 1: DeepSeek Chat (純文本)")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你係一個專業營養師。"},
            {"role": "user", "content": "麥片嘅營養成份係咩？"}
        ]
    }
    
    url = f"{BASE_URL}/chat/completions"
    
    try:
        print("📝 正在調用 DeepSeek API...")
        print("-" * 60)
        
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
            
            print("✅ DeepSeek Chat API 正常！")
            print("\n📝 AI 回答：")
            print(answer)
            
            if "usage" in result:
                usage = result["usage"]
                print(f"\n📊 Token 使用量:")
                print(f"   總計：{usage.get('total_tokens', 'N/A')} tokens")
            
            return True
        else:
            print(f"❌ API 回應異常：{result}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP 錯誤：{e.code}")
        print(f"   錯誤：{e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
        return False

def test_deepseek_vl(image_path: str):
    """測試 2: DeepSeek-VL 圖片識別"""
    print("\n" + "=" * 60)
    print("🧪 測試 2: DeepSeek-VL (圖片識別)")
    print("=" * 60)
    print(f"📸 圖片：{image_path}")
    
    # 讀取圖片並轉為 Base64
    try:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{image_data}"
        print("✅ 圖片載入成功")
    except Exception as e:
        print(f"❌ 圖片載入失敗：{e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # DeepSeek-VL 支援多模態輸入
    payload = {
        "model": "deepseek-chat",  # DeepSeek 新版支援圖片
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": "這張圖片中有什麼食物？請詳細描述，並估計營養成份（卡路里、蛋白質、脂肪、碳水化合物）。"}
            ]
        }]
    }
    
    url = f"{BASE_URL}/chat/completions"
    
    try:
        print("\n📡 正在調用 DeepSeek-VL API...")
        print("-" * 60)
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        # 解析結果
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            
            print("\n✅ DeepSeek-VL API 調用成功！")
            print("\n📝 AI 回答：")
            print("-" * 60)
            print(answer)
            print("-" * 60)
            
            if "usage" in result:
                usage = result["usage"]
                print(f"\n📊 Token 使用量:")
                print(f"   輸入：{usage.get('prompt_tokens', 'N/A')} tokens")
                print(f"   輸出：{usage.get('completion_tokens', 'N/A')} tokens")
                print(f"   總計：{usage.get('total_tokens', 'N/A')} tokens")
            
            print("\n" + "=" * 60)
            print("🎉 測試成功！DeepSeek 支援圖片上傳！")
            print("=" * 60)
            return True
        else:
            print(f"❌ API 回應異常：{result}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP 錯誤：{e.code}")
        error_body = e.read().decode('utf-8')
        print(f"   錯誤訊息：{error_body}")
        
        if e.code == 400:
            print("\n⚠️  DeepSeek 可能唔支援圖片輸入！")
            print("   DeepSeek 主要係文本模型，視覺功能可能有限。")
        return False
    except urllib.error.URLError as e:
        print(f"\n❌ 網絡錯誤：{e.reason}")
        return False
    except Exception as e:
        print(f"\n❌ 未知錯誤：{e}")
        return False

def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("🍎 DeepSeek API 測試工具")
    print("=" * 60)
    print(f"📍 API 端點：{BASE_URL}")
    
    # 測試 1: 純文本
    text_test_passed = test_deepseek_chat()
    
    if not text_test_passed:
        print("\n⚠️  純文本測試失敗！請檢查 API Key。")
        return
    
    # 準備測試圖片
    if len(sys.argv) < 2:
        print("\n⚠️  請提供圖片路徑！")
        print("   用法：python3 test_deepseek_vl.py <圖片路徑>")
        return
    
    image_path = sys.argv[1]
    
    # 測試 2: 圖片識別
    vl_test_passed = test_deepseek_vl(image_path)
    
    # 總結
    print("\n\n" + "=" * 60)
    print("📊 測試總結")
    print("=" * 60)
    print(f"✅ DeepSeek Chat: {'通過' if text_test_passed else '失敗'}")
    print(f"{'✅' if vl_test_passed else '❌'} DeepSeek-VL: {'通過' if vl_test_passed else '失敗'}")
    
    if text_test_passed and vl_test_passed:
        print("\n🎉 恭喜！DeepSeek 完全支援圖片上傳！")
        print("   你可以用 DeepSeek 開發營養師 App！🚀")
    elif text_test_passed and not vl_test_passed:
        print("\n⚠️  純文本 OK，但圖片失敗。")
        print("   DeepSeek 主要係文本模型，建議用阿里雲 Qwen-VL 或 GPT-4V。")
    else:
        print("\n❌ 測試失敗，請檢查 API Key 或聯絡 DeepSeek 支援。")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not image_path:
        print("用法：python3 test_deepseek_vl.py <圖片路徑>")
        sys.exit(1)
    main()
