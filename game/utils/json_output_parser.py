"""
从字符串中提取用markdown代码块包裹的json结果。

一般面对的情况是：指定LLM进行结构化输出，需要从中提取结果。
"""

import json
import re

from typing import Type
from pydantic import BaseModel


class JsonOutputParser:
    """
    这是一个工具类，用于提取LLM的结构化输出。
    所有方法都是无状态的。
    """
    def __init__(self):
        """无论是否实例化都可以使用。"""

    @staticmethod
    def extract_json_from_str(
            response: str,
            need_schema_check: bool = False,
            schema_model: Type[BaseModel] = None,
    ) -> dict | None:
        """
        从字符串格式中提取json格式的输出结果。
        主要使用的是正则方法进行提取，默认以及规范的做法是从markdown代码块中提取。

        Args:
            - response: LLM输出的str部分。
            - need_schema_check: 是否进行schema检验。
            - schema_model: pydantic定义的数据类。上一步设置为True时，这个参数必须要传入。
        Return:
            - 如果没有问题，输出dict的结果。
            - 如果解析失败，输出None。可能有多种原因，或许需要重试机制（最简单，也是这个类的目的。）。
        """
        # 正则匹配
        pattern = r'```json(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        # print(matches)
        # 如果没有找到。一般在prompt中指定，就不会发生这种情况。
        if not matches:
            print("无json输出。")
            return None
        # 提取结果。可能需要根据任务而定。
        raw_data_str: str = matches[-1]
        # 转换为dict
        if not JsonOutputParser.check_json_format(raw_data_str):
            # 进行格式检测，确保是可以转换为dict的。
            return None
        json_data = json.loads(raw_data_str)
        if need_schema_check and not JsonOutputParser.check_schema(schema_model=schema_model, json_data=json_data):
            # 如果需要schema检验，而检验未通过。
            return None
        return json_data

    @staticmethod
    def check_json_format(json_str: str) -> bool:
        """
        一些情况下，LLM输出会带有奇怪格式。进行加载检验。
        """
        """
        TODO: 可以使用一些非严格的json工具，可以自动进行修正。
        """
        try:
            json.loads(json_str)
        except Exception as e:
            print(e)
            print(json_str)
            print("未通过format检验。")
            return False
        return True

    @staticmethod
    def check_schema(schema_model: Type[BaseModel], json_data: dict) -> bool:
        """
        对于已经可以加载的json数据进行字段检验。
        默认使用pydantic，原因在于：
            - 实际的严格检验。
            - 可以处理number和bool数据的自动转换，会很方便。

        Args:
            - schema_model: pydantic定义的数据类。
            - json_data: json数据，实际上这一步已经是python的dict的数据。
        """
        try:
            schema_model(**json_data)
        except Exception as e:
            print(e)
            print(json_data)
            print("未通过schema检验。")
            return False
        return True

