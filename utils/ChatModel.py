#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2024/9/18 09:51
# @File    : ChatModel
# @desc    : 聊天模型类


import os
from dotenv import load_dotenv
load_dotenv()

import Agently

class ChatModel:
    # 创建agent
    def get_agent_factory(self, model_source=os.getenv("MODEL_SOURCE")):
        if model_source == "deepseek":
            agent_factory = Agently.AgentFactory()
            (
                agent_factory
                .set_settings("current_model", "OAIClient")
                .set_settings("model.OAIClient.auth", {"api_key": os.getenv("DEEPSEEK_API_KEY")})
                .set_settings("model.OAIClient.url", os.getenv("DEEPSEEK_API_BASE"))
                .set_settings("model.OAIClient.options", {"model": "deepseek-reasoner", "temperature": 1.3, "max_tokens": 8000})
                .set_settings("is_debug", False)
            )
        if model_source == "gpt":
            agent_factory = Agently.AgentFactory()
            (
                agent_factory
                .set_settings("current_model", "OAIClient")
                .set_settings("model.OAIClient.auth", {"api_key": os.getenv("OPENROUTER_API_KEY")})
                .set_settings("model.OAIClient.url", os.getenv("OPENROUTER_API_BASE"))
                .set_settings("model.OAIClient.options",
                              {"model": "openai/gpt-4o-2024-11-20", "temperature": 0.6, "max_tokens": 4096})
                .set_settings("is_debug", False)
            )
        if model_source == "claude":
            agent_factory = Agently.AgentFactory()
            (
                agent_factory
                .set_settings("current_model", "OAIClient")
                .set_settings("model.OAIClient.auth", {"api_key": os.getenv("OPENROUTER_API_KEY")})
                .set_settings("model.OAIClient.url", os.getenv("OPENROUTER_API_BASE"))
                .set_settings("model.OAIClient.options", {"model": "anthropic/claude-3-5-haiku-20241022", "temperature": 0.7})
                .set_settings("is_debug", False)
            )
        if model_source == "doubao_deepseek":
            agent_factory = Agently.AgentFactory()
            (
                agent_factory
                .set_settings("current_model", "OAIClient")
                .set_settings("model.OAIClient.auth", {"api_key": os.getenv("DOUBAO_API_KEY")})
                .set_settings("model.OAIClient.url", "https://ark.cn-beijing.volces.com/api/v3")
                .set_settings("model.OAIClient.options", {"model": os.getenv('DOUBAO_DEEPSEEK_V3'), "temperature": 0.7})
                .set_settings("is_debug", False)
            )
        if model_source == "doubao":
            agent_factory = Agently.AgentFactory()
            (
                agent_factory
                .set_settings("current_model", "OAIClient")
                .set_settings("model.OAIClient.auth", {"api_key": os.getenv("DOUBAO_API_KEY")})
                .set_settings("model.OAIClient.url", "https://ark.cn-beijing.volces.com/api/v3")
                .set_settings("model.OAIClient.options", {"model": os.getenv('DOUBAO_1.5_PRO_32K'), "temperature": 0.7})
                .set_settings("is_debug", False)
            )
        return agent_factory


if __name__ == '__main__':
    agent_factory = ChatModel().get_agent_factory(model_source="doubao_deepseek")
    agent = agent_factory.create_agent()
    print(
        agent
        .input("给我输出3个单词和2个句子")
        .instruct("输出语言", "中文")
        .output({
            "单词": [("str",)],  # 没有<desc>可省略
            "句子": ("list",),
        })
        .start()
    )