"""
实验参与者的设定。

这是一个完全可以复用于任何任务的agent的模板。
"""

from game.protocols import (
    ManagerRequest,
    ParticipantConfig,
    ParticipantStructuredOutput,
    ParticipantResponse,
)

from autogen_core import (
    RoutedAgent,
    MessageContext,
    TopicId,
    AgentId,
    message_handler,
    type_subscription,
)
from autogen_core.models import (
    SystemMessage,
    AssistantMessage,
    UserMessage,
    LLMMessage,
)
from autogen_core.model_context import UnboundedChatCompletionContext, BufferedChatCompletionContext
from autogen_ext.models.openai import OpenAIChatCompletionClient

import re
import json
from pydantic import BaseModel
from typing import Type, Callable


# @type_subscription(topic_type='manager_request')
class Participant(RoutedAgent):
    """
    试验的参与者。
    可以进行：
        - 分析之前试验的结果。
        - 做出预期。
        - 返回结构化的分析和选择结果。
    """
    def __init__(
        self,
        description: str,
        model_client: OpenAIChatCompletionClient,
        structured_output_format: Type[BaseModel],  # 结构化输出格式的schema，默认使用pydantic。
        prompt_factory,  # 获取各种prompt的工厂，标准且更强大的格式化方法。
        config: dict | None = None,  # 存放各种如prompt template，重构相关方法进行获取。
    ):
        super().__init__(description)
        self._model_client = model_client
        self._structured_output_format = structured_output_format
        self._config = dict(
            _PARTICIPANT_MAX_RETRIES=10,
            _IS_UNLIMITED_CONTEXT_LENGTH=True,
            _CONTEXT_LENGTH=10,
        ) if config is None else config

        self._prompt_factory = prompt_factory
        self._model_context = (
            UnboundedChatCompletionContext()
            if self._config['_IS_UNLIMITED_CONTEXT_LENGTH']
            else BufferedChatCompletionContext(buffer_size=self._config['_CONTEXT_LENGTH'])
        )
        self._system_prompts: list[LLMMessage] = self._get_system_prompts()

    @message_handler
    async def on_manager_request(self, message: ManagerRequest, context: MessageContext) -> ParticipantResponse:
        print(f"{self.id.key}进行选择")
        # 维护模型上下文。
        await self._model_context.add_message(UserMessage(content=message.content, source='manager'))
        # 调用LLM进行响应。
        response = ""
        for i in range(self._config['_PARTICIPANT_MAX_RETRIES']):
            # print(f"第{i}次尝试生成。")
            # 进行最多10次尝试，需要返回的结果是符合通讯协议的。
            response = await self.request_llm(message, context)
            # print(response)
            result = self._extract_json_response(response)
            if result:
                if self._check_schema(self._structured_output_format, result):
                    break
        # 维护模型上下文。
        await self._model_context.add_message(AssistantMessage(content=response, source=self.id.key))
        # 发布选择结果。
        print(f"{self.id.key}的选择：\n{response}")
        await self.publish_message(
            message=ParticipantResponse(
                participant_id=self.id.key,
                content=response,
                result=self._extract_json_response(response)
            ),
            topic_id=TopicId(type='participant_result', source=self.id.key)
        )
        # 返回manager可解析的协议数据。
        return ParticipantResponse(
            participant_id=self.id.key,
            content=response,
            result=self._extract_json_response(response)
        )

    async def request_llm(self, message: ManagerRequest, context: MessageContext) -> str:
        """
        对于LLM client进行请求。默认是有状态的。

        Return: 仅响应的字符串部分。
        """
        llm_result = await self._model_client.create(
            messages=self._system_prompts + await self._model_context.get_messages(),
            cancellation_token=context.cancellation_token,
        )
        response: str = llm_result.content
        # print(response)
        return response

    def _get_system_prompts(self) -> list[LLMMessage]:
        """
        获取system_prompt的方法。
        TODO: 这个方法可能需要频繁重构，之后会设计为抽象方法。

        返回list形式，可以通过context相关的方法直接获取和处理。
        可以使用self.id.key来指定具体每个agent的身份。
        """
        # return [SystemMessage(content=self._config.system_prompt_template)]
        # get_system_prompt_func: Callable = self._config['get_system_prompt_func']
        # system_prompt: str = get_system_prompt_func(
        #     self._config['round_game_setting'],
        #     self._config['participant_attributes'][self.id.key]
        # )
        system_prompt: str = self._prompt_factory.get_system_prompt(agent_id=self.id.key)
        return [SystemMessage(content=system_prompt)]
        # return [SystemMessage(content=self._config.system_prompt_template.format(role=self.id.key))]

    def _get_inference_prompt_template(self, game_round: int) -> str:
        """
        获得inference prompt template的方法。
        """
        # self._config.inference_prompt_template
        inference_prompt: str = self._prompt_factory.get_inference_prompt_template(game_round=game_round)
        return inference_prompt

    def _extract_json_response(self, response: str) -> dict | None:
        pattern = r'```json(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        if not matches:
            return None
        raw_data_str: str = matches[-1]
        try:
            json.loads(raw_data_str)
        except Exception as e:
            print(e)
            return None
        return json.loads(raw_data_str)

    def _check_schema(self, schema_model: Type[BaseModel], json_data: dict) -> bool:
        try:
            schema_model(**json_data)
        except Exception as e:
            print(e)
            print(json_data)
            print("LLM的输出未通过schema检验，进行重试...")
            return False
        return True

