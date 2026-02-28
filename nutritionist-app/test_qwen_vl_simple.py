#!/usr/bin/env python3
"""
Qwen-VL API 簡易測試（無需外部模塊）
"""

import urllib.request
import urllib.error
import json
import base64
import sys

# 配置
API_KEY = "sk-sp-8eec812bc72d47c3866d388cef6372f8"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

def test_qwen_vl(image_path: str):
    """測試 Qwen-VL API"""
    
    print("\n🧪 測試 Qwen-VL API")
    print("=" * 60)
    print(f"📸 圖片：{image_path}")
    print(f"🤖 模型：qwen-vl-plus")
    print("=" * 60)
    
    # 讀取圖片並轉為 Base64
    try:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        image_uri = f"data:image/jpeg;base64,{image_data}"
        print("✅ 圖片載入成功")
    except Exception as e:
        print(f"❌ 圖片載入失敗：{e}")
        return False
    
    # 準備 API 請求
    payload = {
        "model": "qwen-vl-plus",
        "messages": [{
            "role": "user",
            "content": [
                {"image": image_uri},
                {"text": "這張圖片中有什麼食物？請詳細描述，並估計營養成份（卡路里、蛋白質、脂肪、碳水化合物）。"}
            ]
        }]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}/chat/completions"
    
    try:
        print("\n📡 正在調用阿里雲 API...")
        print("-" * 60)
        
        # 發送請求
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
            
            print("\n✅ API 調用成功！")
            print("\n📝 AI 回答：")
            print("-" * 60)
            print(answer)
            print("-" * 60)
            
            # 顯示 Token 使用量
            if "usage" in result:
                usage = result["usage"]
                print(f"\n📊 Token 使用量:")
                print(f"   輸入：{usage.get('input_tokens', 'N/A')} tokens")
                print(f"   輸出：{usage.get('output_tokens', 'N/A')} tokens")
                print(f"   總計：{usage.get('total_tokens', 'N/A')} tokens")
            
            print("\n" + "=" * 60)
            print("🎉 測試成功！阿里雲 Qwen-VL API 完全支援圖片上傳！")
            print("=" * 60)
            return True
        else:
            print(f"❌ API 回應格式異常：{result}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP 錯誤：{e.code}")
        print(f"   錯誤訊息：{e.read().decode('utf-8')}")
        return False
    except urllib.error.URLError as e:
        print(f"\n❌ 網絡錯誤：{e.reason}")
        return False
    except Exception as e:
        print(f"\n❌ 未知錯誤：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 test_qwen_vl_simple.py <圖片路徑>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_qwen_vl(image_path)
    sys.exit(0 if success else 1)
