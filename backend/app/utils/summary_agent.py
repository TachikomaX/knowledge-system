import logging
from typing import Optional

import requests

# 建议将 API_KEY 放在环境变量或配置文件中读取
from app.config import settings

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"  # 官方推荐模型名称

logger = logging.getLogger(__name__)


def generate_summary(note_title: str,
                     note_content: str,
                     max_length: int = 100) -> Optional[str]:
    """
    调用 DeepSeek API 同步生成笔记摘要。
    :param note_content: 笔记正文内容
    :param max_length: 摘要最大长度（字符数）
    :return: 摘要字符串 或 None（失败时）
    """
    if not note_content.strip():
        return None

    prompt = f"""
请为以下笔记内容生成一个简洁的中文摘要，长度不超过 {max_length} 字。
要求：准确、自然、有逻辑，不添加主观评价。

笔记标题：{note_title}
笔记内容：
{note_content}
"""

    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model":
        DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "你是一个帮助生成中文笔记摘要的助手。"
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        "temperature":
        0.3,  # 稳定输出
        "max_tokens":
        512,
    }

    try:
        response = requests.post(DEEPSEEK_API_URL,
                                 headers=headers,
                                 json=payload,
                                 timeout=15)
        response.raise_for_status()
        data = response.json()
        summary = data["choices"][0]["message"]["content"].strip()
        return summary

    except Exception as e:
        logger.error(f"DeepSeek summary generation failed: {e}")
        return None
