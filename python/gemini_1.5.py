#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 客戶端
使用 Google Gemini AI 進行對話和文本生成
"""
import requests

# 替換成你的 Gemini API Key
GEMINI_API_KEY = "AIzaSyD-B4i0umJNkjh-5EwDAcNKSiKpAz77Xk8"

# Gemini API URL (一樣對應 1.5-flash-latest)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# 你要丟給 Gemini 的 Prompt
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "用一句話介紹台積電"
                }
            ]
        }
    ]
}

# POST 請求
response = requests.post(url, json=payload)

# 印出 Gemini 回傳結果
print(response.status_code)
print(response.json())