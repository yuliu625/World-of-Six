from autogen_ext.models.openai import OpenAIChatCompletionClient

import os
from enum import Enum


class QwenModelName(Enum):
    qwen_15 = 'qwen2.5-1.5b-instruct'
    qwen_max = 'qwen-max'
    qwen_plus = 'qwen-plus'
    qwen_turbo = 'qwen-turbo'


class DeepseekModelName(Enum):
    deepseek_chat = 'deepseek-chat'
    deepseek_reasoner = 'deepseek-reasoner'


def get_qwen(model: str = 'qwen2.5-1.5b-instruct'):
    model_client = OpenAIChatCompletionClient(
        model=model,
        base_url=os.environ['DASHSCOPE_API_BASE_URL'],
        api_key=os.environ['DASHSCOPE_API_KEY'],
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": 'unknown',
        },
    )
    return model_client


class ModelClientFactory:
    def get_qwen(self, model: str = 'qwen2.5-1.5b-instruct'):
        model_client = OpenAIChatCompletionClient(
            model=model,
            base_url=os.environ['DASHSCOPE_API_BASE_URL'],
            api_key=os.environ['DASHSCOPE_API_KEY'],
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": False,
                "family": 'unknown',
            },
        )
        return model_client

    def get_deepseek(self, model: str = 'deepseek-reasoner'):
        model_client = OpenAIChatCompletionClient(
            model=model,
            base_url=os.environ['DEEPSEEK_API_BASE_URL'],
            api_key=os.environ['DEEPSEEK_API_KEY'],
            model_info={
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": 'r1',
            },
        )
        return model_client

