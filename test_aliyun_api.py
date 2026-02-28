#!/usr/bin/env python3
"""
測試阿里雲Coding Plan API連接
"""

import os
import requests
import json

def test_aliyun_api():
    """測試阿里雲API連接"""
    
    # 獲取API密鑰
    api_key = os.getenv('ALIYUN_API_KEY')
    if not api_key:
        print("❌ 未找到ALIYUN_API_KEY環境變量")
        return False
    
    print(f"🔑 API密鑰: {api_key[:10]}...{api_key[-4:]}")
    
    # API端點
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    chat_url = f"{base_url}/chat/completions"
    
    # 請求頭
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 請求數據
    data = {
        "model": "qwen-turbo-latest",
        "messages": [
            {"role": "system", "content": "你是一個有用的助手。"},
            {"role": "user", "content": "你好！請簡單回應以確認API連接正常。"}
        ],
        "max_tokens": 50
    }
    
    print(f"🌐 測試API連接: {base_url}")
    print(f"📝 使用模型: {data['model']}")
    
    try:
        # 發送請求
        response = requests.post(chat_url, headers=headers, json=data, timeout=30)
        
        print(f"📊 響應狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API連接成功！")
            print(f"🤖 AI回應: {result.get('choices', [{}])[0].get('message', {}).get('content', '無內容')}")
            return True
        else:
            print(f"❌ API請求失敗: {response.status_code}")
            print(f"錯誤信息: {response.text[:200]}")
            
            # 嘗試解析錯誤
            try:
                error_data = response.json()
                print(f"錯誤詳情: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
            except:
                pass
                
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 請求超時")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 連接錯誤")
        return False
    except Exception as e:
        print(f"❌ 未知錯誤: {e}")
        return False

def check_api_models():
    """檢查可用的模型"""
    
    api_key = os.getenv('ALIYUN_API_KEY')
    if not api_key:
        return
    
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    models_url = f"{base_url}/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    print(f"\\n🔍 檢查可用模型: {models_url}")
    
    try:
        response = requests.get(models_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            models_data = response.json()
            print("✅ 成功獲取模型列表")
            
            if 'data' in models_data:
                print(f"📋 可用模型 ({len(models_data['data'])}個):")
                for model in models_data['data']:
                    print(f"  • {model.get('id', '未知')}")
            else:
                print(f"模型數據格式: {json.dumps(models_data, ensure_ascii=False, indent=2)[:500]}")
        else:
            print(f"❌ 無法獲取模型列表: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 檢查模型時出錯: {e}")

def main():
    """主函數"""
    print("🔧 阿里雲Coding Plan API測試")
    print("=" * 60)
    
    # 測試API連接
    success = test_aliyun_api()
    
    # 檢查可用模型
    if success:
        check_api_models()
    
    print("\\n" + "=" * 60)
    
    if success:
        print("🎉 測試完成！API設置正確，可以開始使用阿里雲Coding Plan。")
        print("💡 建議: 在OpenClaw中切換到阿里雲模型進行測試")
    else:
        print("⚠️  測試失敗，請檢查:")
        print("   1. API密鑰是否正確")
        print("   2. 是否已訂閱Coding Plan服務")
        print("   3. 網絡連接是否正常")
        print("   4. API地址是否正確: https://coding.dashscope.aliyuncs.com/v1")
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())