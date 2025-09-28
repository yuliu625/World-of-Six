"""
关于manager的设定。

这里，不需要基于LLM的manager，基于固定算法的设定会更可靠。
"""

from game.protocols import (
    GameRequest,
    ManagerRequest,
    ParticipantResponse
)
from game.protocols import (
    ParticipantAttribute,
    ParticipantChoice,
    ParticipantChoiceAndPayoff,
)
from game.prompts import BaseParticipantPromptFactory
from game.tools import (
    UtilityCalculator,
    ContextController,
    GameHistoryController,
)

from autogen_core import (
    RoutedAgent,
    MessageContext,
    TopicId,
    AgentId,
    message_handler,
    type_subscription,
)

import re
import json
from pathlib import Path
import inspect
from pydantic import BaseModel
from typing import List, Callable, Type, Tuple

import asyncio

_IS_BATCH_RUN_A_ROUND = True


# @type_subscription(topic_type='game_request')
# @type_subscription(topic_type='participant_response')
class Manager(RoutedAgent):
    """
    一轮试验的控制者。
    会进行：
        - 初始化游戏设定。
        - 进行每一轮试验。
        - 收集试验结果。
    """
    def __init__(
        self,
        description: str,
        participant_attributes: dict[str, dict],
        network_effect: dict[str, float],
        prices: list[dict],
        calculate_utility_func: Callable,  # 效用计算函数
        prompt_factory: BaseParticipantPromptFactory,
        # prompt_factory_class: type[BaseParticipantPromptFactory],  # 获取各种prompt的工厂，标准且更强大的格式化方法。
        config: dict,  # 为了保存游戏的设置
    ):
        super().__init__(description)
        self._utility_calculator = UtilityCalculator(calculate_utility_func=calculate_utility_func)
        self._config = config
        self._participant_attributes = participant_attributes
        self._network_effect = network_effect
        self._prices = prices
        print(prices)
        self._participant_ids: List[AgentId] = [
            AgentId(type='participant', key=participant_id) for participant_id, _ in participant_attributes.items()
        ]

        # self._prompt_factory = self.build_prompt_factory(prompt_factory_class)
        self._prompt_factory = prompt_factory
        # 过去所有agent的对话。
        self._game_context_controller = ContextController()
        # 解析和计算后，participant的选择和收益。
        self._game_history_controller = GameHistoryController()

    @message_handler
    async def on_game_request(self, message: GameRequest, context: MessageContext) -> None:
        """设置试验，进行试验。"""
        # 进行多轮试验。
        for game_round in range(1, message.game_round+1):
            print(f"第{game_round}轮实验：")
            if _IS_BATCH_RUN_A_ROUND:
                await self.batch_run_a_round(game_round=game_round)
            else:
                await self.run_a_round(game_round=game_round)
        # 完成实验之后保存设置和结果。
        self.save_result(self._config['dir_to_save'])

    async def batch_run_a_round(
        self,
        game_round: int
    ) -> list[ParticipantChoiceAndPayoff]:
        participant_response_tasks = []
        for i, participant_id in enumerate(self._participant_ids):
            participant_message_content = self.get_participant_message_content(
                participant_id=participant_id.key,
                game_round=game_round
            )
            participant_response_task = self.send_message_to_participant(
                participant_message_content=participant_message_content,
                participant_id=participant_id,
            )
            participant_response_tasks.append(participant_response_task)
        participant_responses: tuple[ParticipantResponse] = await asyncio.gather(*participant_response_tasks)
        [
            self._game_context_controller.add_a_context(game_round, participant_response)
            for participant_response in participant_responses
        ]
        participant_round_choices = [
            ParticipantChoice(
                participant_id=participant_response.participant_id,
                expectation=participant_response.result['expectation'],
            )
            for participant_response in participant_responses
        ]
        round_calculating_properties, round_result = self._calculate_utilities(
            participant_choices=participant_round_choices,
            network_effect=self._network_effect,
            price=self._prices[game_round - 1],
        )
        # 记录结果。
        self._game_history_controller.add_a_round_game_history(game_round, round_calculating_properties)
        return round_result

    async def run_a_round(
        self,
        game_round: int,
    ) -> list[ParticipantChoiceAndPayoff]:
        """
        运行一轮实验。
        """
        # 记录所有agent的选择。逐步记录，因为在所有agent完成选择之后才能计算结果。
        participant_round_choices = []
        for i, participant_id in enumerate(self._participant_ids):
            participant_message_content = self.get_participant_message_content(
                participant_id=participant_id.key,
                game_round=game_round
            )
            participant_response: ParticipantResponse = await self.send_message_to_participant(
                participant_message_content=participant_message_content,
                participant_id=participant_id,
            )
            # 记录agent响应。
            self._game_context_controller.add_a_context(game_round, participant_response)
            # 记录participant的选择。单独提取是为了计算。
            participant_round_choices.append(
                ParticipantChoice(
                    participant_id=participant_id.key,
                    expectation=participant_response.result['expectation'],
                )
            )
        # 当所有的participant完成选择，计算结果
        round_calculating_properties, round_result = self._calculate_utilities(
            participant_choices=participant_round_choices,
            network_effect=self._network_effect,
            price=self._prices[game_round - 1],
        )
        # 记录结果。
        self._game_history_controller.add_a_round_game_history(game_round, round_calculating_properties)
        return round_result

    async def send_message_to_participant(
        self,
        participant_message_content: str,
        participant_id: AgentId
    ) -> ParticipantResponse:
        """
        向一个participant发送一条请求。
        这个方法应独立于manager的逻辑，manager对于请求的内容自行处理。这个方法是为了保持2个agent的通讯协议。
        """
        participant_response: ParticipantResponse = await self.send_message(
            message=ManagerRequest(
                content=participant_message_content,
            ),
            recipient=participant_id,
        )
        return participant_response

    def _calculate_utilities(
        self,
        participant_choices: list[ParticipantChoice],
        network_effect: dict[str, float],
        price: dict,
    ) -> Tuple[list[dict], list[ParticipantChoiceAndPayoff]]:
        return self._utility_calculator.run(
            participant_attributes=self._participant_attributes,
            network_effect=network_effect,
            price=price,
            participant_choices=participant_choices,
        )

    def build_prompt_factory(self, prompt_factory_class) -> BaseParticipantPromptFactory:
        return prompt_factory_class(
            participant_attributes=self._participant_attributes,
            network_effect=self._network_effect,
            round_prices=self._prices,
            prompt_template_config=self._config['prompt_template_config'],
        )

    def get_participant_message_content(
        self,
        participant_id: str,
        game_round: int,
    ) -> str:
        inference_prompt = self._get_participant_inference_prompt(game_round=game_round)
        history_prompt = self._get_history_prompt(participant_id=participant_id, game_round=game_round)
        return history_prompt + inference_prompt

    def _get_participant_inference_prompt(
        self,
        game_round: int,
    ) -> str:
        inference_prompt = self._prompt_factory.get_inference_prompt(game_round=game_round)
        return inference_prompt
        # return "participant_prompt_placeholder"

    def _get_history_prompt(
        self,
        participant_id: str,
        game_round: int,
    ) -> str:
        # 这里由game_history_controller实现会比prompt_factory更好。
        # history_prompt = self._prompt_factory.get_history_prompt(
        #     agent_id=participant_id,
        #     game_round=game_round
        # )
        history_prompt = self._game_history_controller.get_history_prompt(
            agent_id=participant_id,
            game_round=game_round,
        )
        return history_prompt
        # if game_round == 1:
        #     return ""
        # else:
        #     return "history_prompt_placeholder"

    def _transfer_pydantic_to_dict(self, pydantic_data: list[list[Type[BaseModel]]]) -> list[list[dict]]:
        result = []
        for round_data in pydantic_data:
            round_result: list[dict] = []
            for data in round_data:
                round_result.append(data.model_dump())
            result.append(round_result)
        return result

    def save_result(self, dir_to_save: str) -> None:
        # path处理
        dir_to_save = Path(dir_to_save)
        dir_to_save.mkdir(exist_ok=True, parents=True)
        utility_calculate_func_str: str = inspect.getsource(self._utility_calculator.calculate_utility)

        # 以JSON保存
        # with open(dir_to_save / 'game_setting.json', 'w', encoding='utf-8') as f:
        #     json.dump(self._config, f, ensure_ascii=False, indent=4)
        # with open(dir_to_save / 'participant_attributes.json', 'w', encoding='utf-8') as f:
        #     json.dump(self._participant_attributes, f, ensure_ascii=False, indent=4)

        self._game_context_controller.save_context(dir_to_save / 'game_context.json')
        self._game_history_controller.save_history(dir_to_save / 'game_history.json')

