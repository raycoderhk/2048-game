#!/usr/bin/env python3
"""
載入 .env 文件並設置環境變量
用法：python3 load_env.py && python3 nutritionist_openrouter_only.py test.jpg
"""

import os

def load_env(env_file='.env'):
    """載入 .env 文件"""
    if not os.path.exists(env_file):
        print(f"❌ 找不到 {env_file}")
        return False
    
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳過空行和註解
            if not line or line.startswith('#'):
                continue
            # 解析 KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # 設置環境變量
                os.environ[key] = value
                print(f"✅ 設置 {key}")
    
    return True

if __name__ == '__main__':
    success = load_env()
    if success:
        print("\n✅ 環境變量載入成功！")
        print("\n現在可以執行:")
        print("  python3 nutritionist_openrouter_only.py <圖片路徑>")
    else:
        print("\n❌ 環境變量載入失敗！")
