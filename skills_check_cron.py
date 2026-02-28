#!/usr/bin/env python3
"""
技能狀態檢查 Cron Job
定期驗證所有技能的可用性
"""

import json
import sys
import os
from datetime import datetime
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_basic_tools():
    """檢查基本工具"""
    results = []
    
    tools = [
        ("python3", "Python 3", ["--version"]),
        ("pip3", "pip3", ["--version"]),
        ("tesseract", "Tesseract OCR", ["--version"]),
        ("curl", "curl", ["--version"]),
    ]
    
    for cmd, name, args in tools:
        try:
            result = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                results.append({"tool": name, "status": "✅", "version": version})
            else:
                results.append({"tool": name, "status": "❌", "error": f"返回碼: {result.returncode}"})
        except FileNotFoundError:
            results.append({"tool": name, "status": "❌", "error": "未安裝"})
        except Exception as e:
            results.append({"tool": name, "status": "❌", "error": str(e)})
    
    return results

def check_skills_directory():
    """檢查技能目錄"""
    skills_dir = "/home/node/.openclaw/workspace/skills"
    results = []
    
    if not os.path.exists(skills_dir):
        return [{"skill": "目錄", "status": "❌", "error": f"技能目錄不存在: {skills_dir}"}]
    
    results.append({"skill": "目錄", "status": "✅", "path": skills_dir})
    
    # 檢查每個技能
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path):
            skill_info = {"skill": item, "status": "✅"}
            
            # 檢查必要文件
            required_files = ["SKILL.md"]
            missing_files = []
            
            for file in required_files:
                if not os.path.exists(os.path.join(skill_path, file)):
                    missing_files.append(file)
            
            if missing_files:
                skill_info["status"] = "⚠️"
                skill_info["warning"] = f"缺失文件: {', '.join(missing_files)}"
            
            results.append(skill_info)
    
    return results

def check_smart_ocr_skill():
    """檢查 smart_ocr 技能"""
    skill_path = "/home/node/.openclaw/workspace/skills/smart_ocr"
    results = []
    
    if not os.path.exists(skill_path):
        return [{"component": "smart_ocr", "status": "❌", "error": "技能目錄不存在"}]
    
    # 檢查文件
    required_files = [
        "ocr_tool.py",
        "run_ocr.sh", 
        "tesseract_tool.py",
        "run_tesseract.sh",
        "ocr_venv/bin/python3"
    ]
    
    for file in required_files:
        file_path = os.path.join(skill_path, file)
        if os.path.exists(file_path):
            results.append({"component": file, "status": "✅", "path": file_path})
        else:
            results.append({"component": file, "status": "❌", "error": f"文件不存在: {file_path}"})
    
    # 測試Python環境
    venv_python = os.path.join(skill_path, "ocr_venv/bin/python3")
    if os.path.exists(venv_python):
        try:
            test_script = """
import pytesseract
from PIL import Image
import numpy as np
print('SUCCESS: All imports work')
            """
            
            result = subprocess.run(
                [venv_python, "-c", test_script],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=skill_path
            )
            
            if "SUCCESS" in result.stdout:
                results.append({"component": "Python環境", "status": "✅", "details": "所有依賴正常"})
            else:
                results.append({"component": "Python環境", "status": "❌", "error": f"導入錯誤: {result.stderr[:100]}"})
        except Exception as e:
            results.append({"component": "Python環境", "status": "❌", "error": str(e)})
    
    return results

def check_network_connectivity():
    """檢查網絡連接"""
    results = []
    
    # 測試Yahoo Finance
    try:
        test_url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        import urllib.request
        import urllib.error
        
        req = urllib.request.Request(test_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                results.append({"service": "Yahoo Finance API", "status": "✅", "response": "200 OK"})
            else:
                results.append({"service": "Yahoo Finance API", "status": "❌", "error": f"HTTP {response.status}"})
    except Exception as e:
        results.append({"service": "Yahoo Finance API", "status": "❌", "error": str(e)})
    
    # 測試一般連接
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            results.append({"service": "網絡連接", "status": "✅", "details": "Ping成功"})
        else:
            results.append({"service": "網絡連接", "status": "⚠️", "warning": "Ping失敗"})
    except Exception as e:
        results.append({"service": "網絡連接", "status": "❌", "error": str(e)})
    
    return results

def generate_report(results):
    """生成報告"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "basic_tools": results["basic_tools"],
        "skills": results["skills"],
        "smart_ocr": results["smart_ocr"],
        "network": results["network"]
    }
    
    # 計算統計
    total_checks = 0
    success_count = 0
    warning_count = 0
    error_count = 0
    
    for category in ["basic_tools", "skills", "smart_ocr", "network"]:
        for item in results[category]:
            total_checks += 1
            if item["status"] == "✅":
                success_count += 1
            elif item["status"] == "⚠️":
                warning_count += 1
            elif item["status"] == "❌":
                error_count += 1
    
    report["summary"] = {
        "total_checks": total_checks,
        "success": success_count,
        "warnings": warning_count,
        "errors": error_count,
        "success_rate": (success_count / total_checks * 100) if total_checks > 0 else 0
    }
    
    return report

def print_human_report(report):
    """打印人類可讀的報告"""
    print("🔧 技能狀態檢查報告")
    print("=" * 60)
    print(f"檢查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 基本工具
    print("\n1. 基本工具:")
    print("-" * 40)
    for tool in report["basic_tools"]:
        print(f"{tool['status']} {tool['tool']}: {tool.get('version', tool.get('error', 'OK'))}")
    
    # 技能目錄
    print("\n2. 技能目錄:")
    print("-" * 40)
    for skill in report["skills"]:
        status_msg = skill.get('path', skill.get('warning', skill.get('error', 'OK')))
        print(f"{skill['status']} {skill['skill']}: {status_msg}")
    
    # smart_ocr 技能
    print("\n3. smart_ocr 技能:")
    print("-" * 40)
    for component in report["smart_ocr"]:
        status_msg = component.get('path', component.get('details', component.get('error', 'OK')))
        print(f"{component['status']} {component['component']}: {status_msg}")
    
    # 網絡連接
    print("\n4. 網絡連接:")
    print("-" * 40)
    for service in report["network"]:
        status_msg = service.get('details', service.get('response', service.get('error', service.get('warning', 'OK'))))
        print(f"{service['status']} {service['service']}: {status_msg}")
    
    # 總結
    summary = report["summary"]
    print("\n📊 檢查總結:")
    print("-" * 40)
    print(f"總檢查項目: {summary['total_checks']}")
    print(f"成功: {summary['success']} ({summary['success_rate']:.1f}%)")
    print(f"警告: {summary['warnings']}")
    print(f"錯誤: {summary['errors']}")
    
    if summary['errors'] == 0 and summary['warnings'] == 0:
        print("\n🎉 所有檢查通過！系統狀態良好。")
        return 0
    elif summary['errors'] == 0:
        print("\n👍 系統基本正常，有少量警告需要注意。")
        return 1
    else:
        print(f"\n🔧 發現 {summary['errors']} 個錯誤需要修復。")
        return 2

def save_report(report):
    """保存報告到文件"""
    report_dir = "/home/node/.openclaw/workspace/memory/skill_checks"
    os.makedirs(report_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"skill_check_{timestamp}.json")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 也保存簡要版本到日誌
    log_file = os.path.join(report_dir, "latest_check.log")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"檢查時間: {report['timestamp']}\n")
        f.write(f"成功: {report['summary']['success']}/{report['summary']['total_checks']}\n")
        f.write(f"錯誤: {report['summary']['errors']}\n")
        f.write(f"警告: {report['summary']['warnings']}\n")
    
    return report_file

def main():
    """主函數"""
    print("開始技能狀態檢查...")
    
    # 執行所有檢查
    results = {
        "basic_tools": check_basic_tools(),
        "skills": check_skills_directory(),
        "smart_ocr": check_smart_ocr_skill(),
        "network": check_network_connectivity()
    }
    
    # 生成報告
    report = generate_report(results)
    
    # 打印報告
    exit_code = print_human_report(report)
    
    # 保存報告
    report_file = save_report(report)
    print(f"\n📁 詳細報告已保存至: {report_file}")
    
    # 如果有錯誤，提供修復建議
    if report["summary"]["errors"] > 0:
        print("\n🔧 修復建議:")
        print("-" * 40)
        
        # 檢查具體錯誤
        for category in ["basic_tools", "skills", "smart_ocr", "network"]:
            for item in results[category]:
                if item["status"] == "❌":
                    print(f"問題: {item.get('tool', item.get('skill', item.get('component', item.get('service', '未知'))))}")
                    print(f"  錯誤: {item.get('error', '未知錯誤')}")
                    
                    # 提供修復建議
                    if "未安裝" in str(item.get('error', '')):
                        if "python3" in str(item.get('tool', '')).lower():
                            print("  建議: apt-get install python3")
                        elif "pip3" in str(item.get('tool', '')).lower():
                            print("  建議: apt-get install python3-pip")
                        elif "tesseract" in str(item.get('tool', '')).lower():
                            print("  建議: apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng")
    
    return exit_code

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n檢查被用戶中斷")
        sys.exit(130)
    except Exception as e:
        print(f"檢查過程中發生錯誤: {e}")
        sys.exit(1)