#!/bin/bash
# 測試技能驗證腳本

echo "🔧 技能驗證測試"
echo "================"
echo "測試時間: $(date)"
echo ""

# 1. 檢查基本工具
echo "1. 基本工具檢查:"
echo "----------------"

# Python
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1)
    echo "✅ Python: $python_version"
else
    echo "❌ Python3 未安裝"
fi

# pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3: $(pip3 --version 2>&1 | head -1)"
else
    echo "❌ pip3 未安裝"
fi

# Tesseract OCR
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract: $(tesseract --version 2>&1 | head -1)"
else
    echo "❌ Tesseract 未安裝"
fi

# curl
if command -v curl &> /dev/null; then
    echo "✅ curl: $(curl --version 2>&1 | head -1)"
else
    echo "❌ curl 未安裝"
fi

echo ""

# 2. 檢查已安裝的技能
echo "2. 已安裝技能檢查:"
echo "------------------"

skills_dir="/home/node/.openclaw/workspace/skills"
if [ -d "$skills_dir" ]; then
    echo "✅ 技能目錄存在: $skills_dir"
    
    for skill in "$skills_dir"/*; do
        if [ -d "$skill" ]; then
            skill_name=$(basename "$skill")
            if [ -f "$skill/SKILL.md" ]; then
                echo "  ✅ $skill_name: SKILL.md 存在"
            else
                echo "  ⚠️  $skill_name: SKILL.md 缺失"
            fi
        fi
    done
else
    echo "❌ 技能目錄不存在"
fi

echo ""

# 3. 測試 smart_ocr 技能
echo "3. smart_ocr 技能測試:"
echo "----------------------"

ocr_skill="$skills_dir/smart_ocr"
if [ -d "$ocr_skill" ]; then
    echo "✅ smart_ocr 技能目錄存在"
    
    # 檢查必要文件
    required_files=("ocr_tool.py" "run_ocr.sh" "tesseract_tool.py" "run_tesseract.sh")
    for file in "${required_files[@]}"; do
        if [ -f "$ocr_skill/$file" ]; then
            echo "  ✅ $file 存在"
        else
            echo "  ❌ $file 缺失"
        fi
    done
    
    # 測試虛擬環境
    if [ -f "$ocr_skill/ocr_venv/bin/python3" ]; then
        echo "  ✅ 虛擬環境存在"
        
        # 測試Python包
        echo "  📦 測試Python包..."
        cd "$ocr_skill"
        if . ocr_venv/bin/activate && python3 -c "import pytesseract; import PIL; print('✅ pytesseract和PIL可用')" 2>/dev/null; then
            echo "  ✅ Python依賴正常"
        else
            echo "  ❌ Python依賴有問題"
        fi
    else
        echo "  ❌ 虛擬環境缺失"
    fi
else
    echo "❌ smart_ocr 技能未安裝"
fi

echo ""

# 4. 測試網絡連接
echo "4. 網絡連接測試:"
echo "----------------"

# 測試Yahoo Finance API
echo "測試Yahoo Finance API連接..."
if curl -s "https://query1.finance.yahoo.com/v8/finance/chart/AAPL" -H "User-Agent: Mozilla/5.0" --max-time 10 2>&1 | grep -q "regularMarketPrice"; then
    echo "✅ Yahoo Finance API 可訪問"
else
    echo "❌ Yahoo Finance API 無法訪問"
fi

# 測試一般網絡
if ping -c 1 -W 2 8.8.8.8 &> /dev/null; then
    echo "✅ 網絡連接正常"
else
    echo "❌ 網絡連接有問題"
fi

echo ""

# 5. 測試文件操作
echo "5. 文件操作測試:"
echo "----------------"

test_file="/tmp/test_skill_$(date +%s).txt"
echo "測試寫入: $test_file"
if echo "技能測試 $(date)" > "$test_file"; then
    echo "✅ 文件寫入成功"
    
    if [ -f "$test_file" ]; then
        echo "✅ 文件存在檢查"
        
        content=$(cat "$test_file" 2>/dev/null)
        if [ -n "$content" ]; then
            echo "✅ 文件讀取成功"
        else
            echo "❌ 文件讀取失敗"
        fi
        
        # 清理
        rm "$test_file"
        echo "✅ 文件清理成功"
    else
        echo "❌ 文件不存在"
    fi
else
    echo "❌ 文件寫入失敗"
fi

echo ""

# 6. 總結
echo "📊 技能驗證總結"
echo "================"

# 計算成功/失敗
success_count=$(grep -c "✅" /tmp/skill_test_output 2>/dev/null || echo 0)
warning_count=$(grep -c "⚠️" /tmp/skill_test_output 2>/dev/null || echo 0)
error_count=$(grep -c "❌" /tmp/skill_test_output 2>/dev/null || echo 0)

echo "✅ 成功: $success_count"
echo "⚠️  警告: $warning_count"
echo "❌ 錯誤: $error_count"

if [ $error_count -eq 0 ]; then
    echo "🎉 所有基本技能測試通過！"
    exit 0
elif [ $error_count -le 2 ]; then
    echo "👍 大部分技能正常，有少量問題需要修復"
    exit 1
else
    echo "🔧 有多個技能問題需要修復"
    exit 2
fi