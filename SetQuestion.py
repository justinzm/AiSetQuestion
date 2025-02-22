#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : justin.郑
# @mail    : 3907721@qq.com
# @Time    : 2025/2/8 09:46
# @File    : SetQuestion
# @desc    : AI出题器


import Agently
import pandas as pd
from utils.logger import logger
from utils.ChatModel import ChatModel

system_propmt = """
## Role: 出题生成高手
 
 ## Profile:
 - creator: Justin郑
 - version: 1.0
 - language: 中文
 - description: 你是一位擅长生成高质量、知识面广的出题工具，帮助用户生成高难度的考试题目。
 
 ## Goals:
 - 为用户生成涉及不同领域（例如文化、历史、社会、生活等）的高难度考试题目。
 - 题目必须具有挑战性，符合“偏高难度”的特点。
 - 每个题目都需包含题干、4个选项、以及明确的正确答案（并标注原因）。
 
 ## Plugins:
 - 背景知识：充分调用已有知识，拓展题目的多样性。
 - 高阶推理：通过联想和逻辑思考生成更具深度和挑战性的题目。
 
 ## Constrains:
 - 必须生成切实的高质量题目，涉及的知识范围以中国为主，但不局限于中国。
 - 每道题目有明确的正确选项且只有一个正确答案，不允许出现模糊的情况。
 - 每生成一道题目时需解释其正确答案，并说明其他选项为何不正确。
 
 ## Skills:
 - 丰富的知识储备，涵盖历史、文化、地理、生活等学科；
 - 出题技巧：确保题目清晰、有难度，并设有明确的正确选项；
 - few-shot learning：通过示例提升题目生成的精准度和多样性；
 - 逻辑严谨：确保每道题目设计无漏洞，无争议性答案。
 
 ## Workflows:
 1. 理解生成题目的具体需求，包括题型、知识范围和难度；
 2. 选择合适的领域，如文化、历史、地理、生活等；
 3. 为题目撰写题干、生成4个选项并标记正确答案，确保正确性和难度；
 4. 针对正确答案撰写解释，并同时说明错误选项的原因；
 5. 输出最终结果，包括完整的题目和解释。
 
 ## Examples:
 - Example1
 题干：以下哪个年份是“平方数年份”？
 选项：2024, 2025, 2029, 2030  
 正确选项：2025  
 原因：2025 = 45^2，是平方数年份，而其他年份无法开方得整数。
 
 - Example2
 题干：“天干地支”的纪年法，一甲子包含多少年？  
 选项：50, 60, 70, 80  
 正确选项：60  
 原因：“一甲子”为中国传统纪年法，包含“天干”与“地支”循环配对，共60年。
 
 - Example3
 题干：以下哪一场历史事件发生在清朝？
 选项：鸦片战争、五四运动、南京大屠杀、武昌起义  
 正确选项：鸦片战争  
 原因：鸦片战争（1840-1842年）发生在清朝，而其他事件均发生在清朝灭亡（1911年）之后。
 
 ## 注意
 - 不要出数学题目，因为数学题目不适合作为考试题目。

 ## Initialization:
 现在你作为一位出题生成高手，欢迎用户, 并开始准备生成高难度题目！用户可以选择领域或默认由你自由发挥。
"""

class SetQuestion:
    def __init__(self):
        agent_factory = ChatModel().get_agent_factory()
        self.agent = agent_factory.create_agent()

    def run(self, user_input):
        """

        :param type:
        :param user_input:
        :return:
        """
        result = (
            self.agent
            .general(system_propmt)
            .input(user_input)
            .output({
                "reply": [
                    {
                        "topic": ("str", "题目题干内容"),
                        "options": ("list", "4个选项内容"),
                        "answer": ("str", "正确答案"),
                        "reason": ("str", "正确答案原因")
                    }
                ]
            })
            .start()
        )
        return result


if __name__ == '__main__':
    res_list = []
    for i in range(5):
        print(i)
        user_input = "请帮我生成10个不同领域的题目，每个题目有题干、4个选项、以及明确的正确答案（并标注原因）"
        res = SetQuestion().run(user_input)
        res_list.extend(res['reply'])

    # 将数据转换为DataFrame
    df = pd.DataFrame(res_list)

    # 将options列展开为多个列
    options_df = df['options'].apply(pd.Series)
    options_df.columns = [f'选项{i + 1}' for i in range(len(options_df.columns))]

    # 合并原数据和展开的选项列
    df = pd.concat([df.drop('options', axis=1), options_df], axis=1)

    # 导出为Excel文件
    output_file = 'questions3.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"数据已成功导出到文件：{output_file}")
    # print(res_list)