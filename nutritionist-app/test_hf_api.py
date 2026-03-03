#!/usr/bin/env python3
"""測試 Hugging Face API 連接"""

import urllib.request
import urllib.error
import json
import os

HF_TOKEN = "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"

# 測試 1: 檢查 Token 是否有效
print("=" * 60)
print("🧪 測試 1: 檢查 HF Token")
print("=" * 60)

try:
    req = urllib.request.Request(
        "https://huggingface.co/api/whoami-v2",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        method="GET"
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode("utf-8"))
        print(f"✅ Token 有效！")
        print(f"用戶：{result.get('name', 'Unknown')}")
        print(f"類型：{result.get('type', 'Unknown')}")
except Exception as e:
    print(f"❌ Token 無效：{e}")

# 測試 2: 測試圖片識別 API
print("\n" + "=" * 60)
print("🧪 測試 2: 測試圖片識別 API")
print("=" * 60)

# 下載測試圖片
print("📥 下載測試圖片...")
urllib.request.urlretrieve(
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
    "test_food.jpg"
)

with open("test_food.jpg", "rb") as f:
    image_data = f.read()

print(f"✅ 圖片載入成功 ({len(image_data)} bytes)")

# 測試模型
models_to_test = [
    "google/siglip-so400m-patch14-384",
    "google/vit-base-patch16-224",
    "facebook/detr-resnet-50",
]

for model_id in models_to_test:
    print(f"\n🤖 測試模型：{model_id}")
    
    try:
        url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
        req = urllib.request.Request(
            url,
            data=image_data,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/octet-stream",
                "User-Agent": "Mozilla/5.0"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"✅ 成功！")
            print(f"結果：{result[:3] if isinstance(result, list) else result}")
            break
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"❌ 錯誤：{e}")

print("\n" + "=" * 60)
print("✅ 測試完成！")
print("=" * 60)
