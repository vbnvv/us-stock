#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 客戶端
使用 Google Gemini AI 進行對話和文本生成
"""

import google.generativeai as genai
import json
import time
import logging
from typing import List, Dict, Any, Optional

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: str):
        """
        初始化 Gemini 客戶端
        
        Args:
            api_key: Gemini API 密鑰
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # 初始化模型
        try:
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini 模型初始化成功")
        except Exception as e:
            logger.error(f"模型初始化失敗: {e}")
            raise
    
    def check_quota(self) -> bool:
        """
        檢查 API 配額狀態
        
        Returns:
            True 如果配額正常，False 如果配額已用完
        """
        try:
            # 嘗試發送一個簡單的測試請求
            response = self.model.generate_content("test", max_output_tokens=10)
            return True
        except Exception as e:
            if "quota" in str(e).lower() or "resource_exhausted" in str(e).lower():
                logger.error("API 配額已用完")
                return False
            else:
                logger.error(f"配額檢查失敗: {e}")
                return False
    
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        生成文本回應
        
        Args:
            prompt: 輸入提示
            max_tokens: 最大生成字數
            temperature: 創意度 (0.0-1.0)
            
        Returns:
            生成的文本
        """
        try:
            logger.info(f"正在生成文本，提示: {prompt[:50]}...")
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            result = response.text
            logger.info(f"文本生成成功，長度: {len(result)} 字符")
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "resource_exhausted" in error_msg.lower():
                return "錯誤: API 配額已用完，請檢查您的計劃和計費詳情。"
            elif "rate" in error_msg.lower():
                return "錯誤: 請求頻率過高，請稍後再試。"
            else:
                logger.error(f"文本生成失敗: {e}")
                return f"錯誤: {error_msg}"
    
    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        進行對話
        
        Args:
            messages: 對話歷史，格式為 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            max_tokens: 最大生成字數
            temperature: 創意度
            
        Returns:
            AI 的回應
        """
        try:
            logger.info(f"開始對話，消息數量: {len(messages)}")
            
            # 創建聊天會話
            chat = self.model.start_chat(history=[])
            
            # 發送最後一條用戶消息
            if messages:
                last_message = messages[-1]
                if last_message.get("role") == "user":
                    response = chat.send_message(
                        last_message["content"],
                        generation_config=genai.types.GenerationConfig(
                            max_output_tokens=max_tokens,
                            temperature=temperature
                        )
                    )
                    result = response.text
                    logger.info(f"對話回應成功，長度: {len(result)} 字符")
                    return result
            
            return "沒有找到用戶消息"
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "resource_exhausted" in error_msg.lower():
                return "錯誤: API 配額已用完，請檢查您的計劃和計費詳情。"
            else:
                logger.error(f"對話失敗: {e}")
                return f"錯誤: {error_msg}"
    
    def analyze_text(self, text: str, analysis_type: str = "summary") -> str:
        """
        分析文本
        
        Args:
            text: 要分析的文本
            analysis_type: 分析類型 ("summary", "sentiment", "keywords", "translation")
            
        Returns:
            分析結果
        """
        prompts = {
            "summary": f"請為以下文本提供簡潔的摘要：\n\n{text}",
            "sentiment": f"請分析以下文本的情感傾向（正面/負面/中性）：\n\n{text}",
            "keywords": f"請從以下文本中提取關鍵詞：\n\n{text}",
            "translation": f"請將以下文本翻譯成中文：\n\n{text}"
        }
        
        prompt = prompts.get(analysis_type, prompts["summary"])
        return self.generate_text(prompt)
    
    def save_conversation(self, messages: List[Dict[str, str]], filename: str = None) -> str:
        """
        保存對話記錄
        
        Args:
            messages: 對話記錄
            filename: 文件名（可選）
            
        Returns:
            保存的文件名
        """
        if not filename:
            filename = f"gemini_conversation_{int(time.time())}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            logger.info(f"對話記錄已保存到: {filename}")
            return filename
        except Exception as e:
            logger.error(f"保存對話記錄失敗: {e}")
            return None
    
    def load_conversation(self, filename: str) -> List[Dict[str, str]]:
        """
        載入對話記錄
        
        Args:
            filename: 文件名
            
        Returns:
            對話記錄
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            logger.info(f"對話記錄已載入: {filename}")
            return messages
        except Exception as e:
            logger.error(f"載入對話記錄失敗: {e}")
            return []

def main():
    """
    主函數 - 演示 Gemini API 功能
    """
    # API 密鑰
    API_KEY = "AIzaSyD-B4i0umJNkjh-5EwDAcNKSiKpAz77Xk8"
    
    try:
        # 初始化客戶端
        client = GeminiClient(API_KEY)
        
        print("="*60)
        print("Gemini AI 客戶端")
        print("="*60)
        
        # 檢查配額
        print("\n檢查 API 配額...")
        if not client.check_quota():
            print("❌ API 配額已用完！")
            print("請訪問 https://ai.google.dev/gemini-api/docs/rate-limits 查看詳情")
            print("或等待配額重置後再試")
            return
        
        print("✅ API 配額正常")
        
        # 測試基本文本生成
        print("\n1. 測試文本生成:")
        prompt = "請用中文介紹一下人工智能的發展歷史"
        response = client.generate_text(prompt)
        print(f"提示: {prompt}")
        print(f"回應: {response}")
        
        # 測試文本分析
        print("\n" + "="*60)
        print("2. 測試文本分析:")
        sample_text = """
        Phillips 66 (PSX) 宣布了到2027年將中游EBITDA有機增長至45億美元的計劃。
        該公司表示，這一增長將通過現有資產的優化、新項目開發和戰略收購來實現。
        分析師對這一計劃持樂觀態度，認為這將為股東創造長期價值。
        """
        
        # 摘要分析
        summary = client.analyze_text(sample_text, "summary")
        print(f"摘要: {summary}")
        
        # 情感分析
        sentiment = client.analyze_text(sample_text, "sentiment")
        print(f"情感分析: {sentiment}")
        
        # 關鍵詞提取
        keywords = client.analyze_text(sample_text, "keywords")
        print(f"關鍵詞: {keywords}")
        
        # 測試對話功能
        print("\n" + "="*60)
        print("3. 測試對話功能:")
        messages = [
            {"role": "user", "content": "你好，請介紹一下你自己"},
            {"role": "assistant", "content": "你好！我是 Gemini，一個由 Google 開發的 AI 助手。"},
            {"role": "user", "content": "你能幫我做什麼？"}
        ]
        
        response = client.chat(messages)
        print(f"AI 回應: {response}")
        
        # 保存對話記錄
        messages.append({"role": "assistant", "content": response})
        filename = client.save_conversation(messages)
        print(f"\n對話記錄已保存到: {filename}")
        
        print("\n" + "="*60)
        print("測試完成！")
        
    except Exception as e:
        print(f"錯誤: {e}")
        logger.error(f"主程序執行失敗: {e}")

if __name__ == "__main__":
    main() 