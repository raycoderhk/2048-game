#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App Web Server
提供 API 接口調用 Hugging Face + Aliyun AI
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import base64
from http import HTTPStatus
from urllib.parse import urlparse

# ============ 配置 ============
PORT = 8080
HF_TOKEN = os.environ.get("HF_API_KEY", "")
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "")

MODEL_ID = "google/siglip-so400m-patch14-384"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# ============ API 處理 ============
def recognize_food(image_data):
    """識別食物圖片 (Hugging Face API)"""
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    
    try:
        req = urllib.request.Request(HF_API_URL, data=image_data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        if isinstance(result, list):
            return {"success": True, "foods": [item.get("label", "") for item in result[:5]]}
        return {"success": True, "foods": [str(result)]}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_nutrition(food_items):
    """分析營養成分 (Aliyun Qwen API)"""
    prompt = f"請分析以下食物的營養成分：{', '.join(food_items)}，以 JSON 格式返回"
    headers = {"Authorization": f"Bearer {ALIYUN_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "qwen3.5-plus", "messages": [{"role": "system", "content": "你是營養師"}, {"role": "user", "content": prompt}]}
    
    try:
        req = urllib.request.Request(ALIYUN_API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        start, end = content.find("{"), content.rfind("}") + 1
        if start >= 0 and end > start:
            return {"success": True, "data": json.loads(content[start:end])}
        return {"success": False, "error": "JSON 解析失敗"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ HTTP Handler ============
class NutritionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path.startswith('/api/'):
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED, "API 需要使用 POST")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)
    
    def do_POST(self):
        if urlparse(self.path).path == '/api/analyze':
            self.handle_analyze()
        else:
            self.send_error(HTTPStatus.NOT_FOUND)
    
    def handle_analyze(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            image_base64 = data.get('image', '')
            if ',' in image_base64: image_base64 = image_base64.split(',')[1]
            image_data = base64.b64decode(image_base64)
            
            recognition = recognize_food(image_data)
            if not recognition.get('success'):
                return self.send_json(recognition)
            
            nutrition = analyze_nutrition(recognition['foods'])
            self.send_json({"success": True, "foods": recognition['foods'], "nutrition": nutrition})
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})
    
    def send_json(self, data):
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    print(f"🥗 營養師 App Server - http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), NutritionHandler) as httpd:
        httpd.serve_forever()
