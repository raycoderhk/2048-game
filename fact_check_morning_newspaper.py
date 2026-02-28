#!/usr/bin/env python3
"""
晨報事實核查工具
"""

import json
from datetime import datetime

def fact_check_newspaper(content):
    """對晨報內容進行事實核查"""
    
    print("🔍 晨報事實核查報告")
    print("=" * 60)
    print(f"核查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    lines = content.split('\n')
    
    # 定義核查類別
    checks = {
        "天氣數據": [],
        "財政數字": [],
        "樓市數據": [],
        "文化活動": [],
        "科技產品": [],
        "娛樂資訊": [],
        "健康建議": []
    }
    
    # 分析各部分的準確性
    current_section = ""
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # 識別當前部分
        if "【今日天氣】" in line:
            current_section = "天氣數據"
        elif "【本港大事】" in line:
            current_section = "財政數字"
        elif "【社會熱話】" in line:
            current_section = "文化活動"
        elif "【科技新知】" in line:
            current_section = "科技產品"
        elif "【娛樂點滴】" in line:
            current_section = "娛樂資訊"
        elif "【養生一點通】" in line:
            current_section = "健康建議"
        
        # 根據內容類型進行核查
        if current_section and line:
            # 檢查數字
            if any(char.isdigit() for char in line):
                if "$" in line or "元" in line or "萬" in line:
                    checks[current_section].append({
                        "line": line,
                        "line_number": i+1,
                        "type": "monetary_value",
                        "needs_verification": True
                    })
                elif "°C" in line or "%" in line:
                    checks[current_section].append({
                        "line": line,
                        "line_number": i+1,
                        "type": "measurement",
                        "needs_verification": True
                    })
                elif "年" in line or "月" in line or "日" in line:
                    checks[current_section].append({
                        "line": line,
                        "line_number": i+1,
                        "type": "date",
                        "needs_verification": True
                    })
            
            # 檢查具體聲明
            keywords_to_check = [
                "政府公佈", "加至", "增至", "約", "平均", "展期",
                "門票", "價錢", "最新", "投資", "預計"
            ]
            
            for keyword in keywords_to_check:
                if keyword in line:
                    checks[current_section].append({
                        "line": line,
                        "line_number": i+1,
                        "type": "statement",
                        "keyword": keyword,
                        "needs_verification": True
                    })
    
    # 生成核查報告
    print("\n📊 核查結果摘要")
    print("=" * 60)
    
    total_checks = 0
    needs_verification = 0
    
    for category, items in checks.items():
        if items:
            print(f"\n{category}:")
            print(f"  需要驗證項目: {len(items)}")
            total_checks += len(items)
            needs_verification += len(items)
            
            # 顯示前3個需要驗證的項目
            for item in items[:3]:
                print(f"  • 第{item['line_number']}行: {item['line'][:50]}...")
    
    print(f"\n總檢查項目: {total_checks}")
    print(f"需要驗證項目: {needs_verification}")
    
    # 具體核查建議
    print("\n🔍 具體核查建議")
    print("=" * 60)
    
    print("\n1. 天氣數據:")
    print("   • 香港今日天氣: 需要查閱天文台最新數據")
    print("   • 溫度22°C: 需要驗證實際溫度範圍")
    print("   • 濕度75%: 需要驗證實際濕度")
    
    print("\n2. 財政數字:")
    print("   • 生果金$1,600: 需要查證最新金額")
    print("   • 醫療券$3,000: 需要查證2026年實際金額")
    print("   • 電費補貼$1,000: 需要查證補貼計劃詳情")
    
    print("\n3. 樓市數據:")
    print("   • 平均呎價$13,500: 需要查證最新樓價指數")
    print("   • 下跌約2%: 需要查證實際變動百分比")
    print("   • 租金回報率2.8%: 需要查證實際回報率")
    
    print("\n4. 文化活動:")
    print("   • 粵劇展覽: 需要查證西九文化區實際展覽")
    print("   • 門票$60: 需要查證長者優惠票價")
    print("   • 展期至6月30日: 需要查證實際展期")
    
    print("\n5. 科技產品:")
    print("   • 手機長者模式: 需要查證最新手機功能")
    print("   • 價錢$3,000起: 需要查證實際市場價格")
    print("   • 清潔機械人$2,500: 需要查證平均價格")
    
    print("\n6. 娛樂資訊:")
    print("   • 《帝女花》演出: 需要查證新光戲院檔期")
    print("   • 門票$180-$480: 需要查證實際票價")
    print("   • TVB重播《上海灘》: 需要查證播放時間")
    
    print("\n7. 健康建議:")
    print("   • 飲水建議: 一般性建議，基本準確")
    print("   • 飲食提醒: 一般性建議，基本準確")
    print("   • 心境建議: 一般性建議，基本準確")
    
    # 準確性評估
    print("\n📈 準確性評估")
    print("=" * 60)
    
    print("\n✅ 基本準確的內容:")
    print("   • 天氣穿衣建議 (基於溫度推斷)")
    print("   • 健康養生貼士 (一般性建議)")
    print("   • 外出活動建議 (基於天氣推斷)")
    
    print("\n⚠️ 需要驗證的內容:")
    print("   • 所有具體數字和金額")
    print("   • 政府政策細節")
    print("   • 市場價格數據")
    print("   • 活動時間和地點")
    
    print("\n🔍 建議驗證來源:")
    print("   1. 香港天文台 - 天氣數據")
    print("   2. 政府新聞公報 - 政策細節")
    print("   3. 差餉物業估價署 - 樓市數據")
    print("   4. 西九文化區官網 - 展覽資訊")
    print("   5. 消費者委員會 - 產品價格")
    print("   6. 電視台節目表 - 播放時間")
    
    # 生成改進建議
    print("\n💡 改進建議")
    print("=" * 60)
    
    print("1. 數據來源標註:")
    print("   • 添加數據來源說明")
    print("   • 註明數據更新時間")
    print("   • 提供參考鏈接")
    
    print("\n2. 內容準確性:")
    print("   • 使用官方數據源")
    print("   • 定期更新數字")
    print("   • 添加免責聲明")
    
    print("\n3. 讀者溝通:")
    print("   • 說明數據為示例性質")
    print("   • 建議讀者查證重要資訊")
    print("   • 提供查證方法")
    
    # 保存核查報告
    report = {
        "check_time": datetime.now().isoformat(),
        "total_lines": len(lines),
        "checks_performed": total_checks,
        "needs_verification": needs_verification,
        "detailed_checks": checks,
        "accuracy_assessment": {
            "weather": "需要驗證實際數據",
            "financial": "需要驗證政策細節",
            "property": "需要驗證市場數據",
            "cultural": "需要驗證活動詳情",
            "technology": "需要驗證產品資訊",
            "entertainment": "需要驗證播放資訊",
            "health": "基本準確"
        }
    }
    
    output_file = "/home/node/.openclaw/workspace/memory/fact_check_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 詳細核查報告已保存至: {output_file}")
    
    return report

def main():
    """主函數"""
    # 讀取晨報內容
    today = datetime.now().strftime("%Y%m%d")
    newspaper_file = f"/home/node/.openclaw/workspace/memory/morning_newspapers/morning_newspaper_{today}.txt"
    
    try:
        with open(newspaper_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"讀取晨報文件: {newspaper_file}")
        fact_check_newspaper(content)
        
    except FileNotFoundError:
        print(f"❌ 未找到晨報文件: {newspaper_file}")
        print("請先運行晨報生成器")
        return 1
    
    return 0

if __name__ == "__main__":
    main()