"""
效用计算器。

无法避免地，计算很复杂并且有多个步骤可能需要可配置。
我尽可能将很多方法写成无状态的，以方便多种情况下使用。
"""

from game.protocols import (
    ParticipantAttribute,
    ParticipantChoice,
    ParticipantChoiceAndPayoff,
)

from typing import Callable, TypedDict, Tuple
from pprint import pprint


class _ParticipantAttribute(TypedDict):
    participant_id: str
    standalone_value: float


class _RoundGameSetting(TypedDict):
    network_benefit: float
    price: float


class _ParticipantChoice(TypedDict):
    participant_id: str
    expectation: int


class _ParticipantParedResult(TypedDict):
    participant_id: str
    standalone_value: float
    network_benefit: float
    price: float
    expectation: int


class UtilityCalculator:
    def __init__(
        self, calculate_utility_func: Callable
    ):
        """
        为了尽可能无状态，计算器仅与效用计算方法绑定。
        Args:
            - calculate_utility_func: 效用计算函数。需要以kwargs形式传递参数，命名需要一致。
        """
        self.calculate_utility_func = calculate_utility_func

    def get_choices_list(self, participant_choices: list[dict]) -> list[bool]:
        """
        这个方法可能在不同输出的情况下被重写。
        仅为了计算参与人数，不是为了得到确定的映射关系。
        """
        return [participant_choice['is_participate'] for participant_choice in participant_choices]

    def calculate_participant_number_by_choices_list(self, choices: list[bool]) -> int:
        """
        当参与情况以bool方式表示时的计算方法。
        """
        return sum(choices)

    def get_real_participant_number(self, participant_choices: list[dict]) -> int:
        """
        计算参与人数的方法。

        默认，participant agent进行数据校验和重新请求，确保choice字段为bool。
        """
        choices_list = self.get_choices_list(participant_choices)
        participant_number = self.calculate_participant_number_by_choices_list(choices_list)
        return participant_number

    def calculate_utility(
        self,
        standalone_value: float,
        network_effect: float,
        participant_number: int,
        price: float,
        is_participate: bool
    ) -> float:
        """
        计算一个participant选择的收益。

        需要这个participant的计算相关属性。
        """
        if is_participate:
            return self.calculate_utility_func(
                standalone_value=standalone_value,
                network_effect=network_effect,
                participant_number=participant_number,
                price=price
            )
        else:
            return 0

    def batch_get_expectation_payoff(self, participant_calculating_properties: list[_ParticipantParedResult]) -> None:
        for i, participant_calculating_property in enumerate(participant_calculating_properties):
            expectation_payoff = self.calculate_utility(
                standalone_value=participant_calculating_property['standalone_value'],
                network_effect=participant_calculating_property['network_effect'],
                price=participant_calculating_property['price'],
                participant_number=participant_calculating_property['expectation'],
                is_participate=True
            )
            participant_calculating_properties[i]['expectation_payoff'] = expectation_payoff
            participant_calculating_properties[i]['is_participate'] = True if expectation_payoff > 0 else False
        # return participant_calculating_properties

    def batch_get_real_payoff(
        self, participant_calculating_properties: list[_ParticipantParedResult],
        real_participant_number: int
    ) -> None:
        for i, participant_calculating_property in enumerate(participant_calculating_properties):
            real_payoff = self.calculate_utility(
                standalone_value=participant_calculating_property['standalone_value'],
                network_effect=participant_calculating_property['network_effect'],
                price=participant_calculating_property['price'],
                participant_number=real_participant_number,
                is_participate=participant_calculating_property['is_participate']
            )
            participant_calculating_properties[i]['real_participant_number'] = real_participant_number
            participant_calculating_properties[i]['real_payoff'] = real_payoff
        # return participant_calculating_properties

    def get_calculating_properties(
        self,
        participant_attribute: _ParticipantAttribute,
        network_effect: dict[str, float],
        price: _RoundGameSetting,
        participant_choice: _ParticipantChoice,
    ) -> _ParticipantParedResult:
        """有3个相关的计算属性的dict，将它们合并在一起。"""
        return participant_attribute | network_effect | price | participant_choice

    def batch_get_calculating_properties(
        self,
        participant_attributes: dict[str, _ParticipantAttribute],
        network_effect: dict[str, float],
        price: _RoundGameSetting,
        participant_choices: list[_ParticipantChoice],
    ) -> list[_ParticipantParedResult]:
        """
        批量将所有的信息合并、转换，成为为更好计算的list。
        Args:
            - participant_attributes: dict的participant的属性，在一整场游戏中是不变的。可以使用id索引。
            - round_game_setting: 游戏的设置，所有的participant是一样的。
            - participant_choices: list的participant的选择，被处理的对象。
        Return: 计算的结果。
        """
        result = []
        for participant_choice in participant_choices:
            participant_attribute = participant_attributes[participant_choice['participant_id']]
            participant_calculating_properties = self.get_calculating_properties(
                participant_attribute=participant_attribute,
                network_effect=network_effect,
                price=price,
                participant_choice=participant_choice,
            )
            result.append(participant_calculating_properties)
        return result

    def batch_get_participant_result(
        self,
        participant_attributes: dict[str, _ParticipantAttribute],
        network_effect: dict[str, float],
        price: _RoundGameSetting,
        participant_choices: list[_ParticipantChoice],
    ) -> Tuple[list[dict], list[ParticipantChoiceAndPayoff]]:
        """
        计算一组participant的效用，映射2种dataclass。
        Args:
            - participant_attributes: 所有participant的计算属性。
            - participant_choices: 所有participant的选择。
        """
        participant_calculating_properties = self.batch_get_calculating_properties(
            participant_attributes=participant_attributes,
            network_effect=network_effect,
            price=price,
            participant_choices=participant_choices,
        )
        # return participant_calculating_properties
        self.batch_get_expectation_payoff(participant_calculating_properties)
        # return participant_calculating_properties
        real_participant_number = self.get_real_participant_number(participant_calculating_properties)
        self.batch_get_real_payoff(participant_calculating_properties, real_participant_number)
        # return participant_calculating_properties
        participant_calculating_properties: list[ParticipantChoiceAndPayoff.model_dump()]
        result = [
            ParticipantChoiceAndPayoff(
                participant_id=participant_calculating_property['participant_id'],
                expectation=participant_calculating_property['expectation'],
                expectation_payoff=participant_calculating_property['expectation_payoff'],
                is_participate=participant_calculating_property['is_participate'],
                real_participant_number=participant_calculating_property['real_participant_number'],
                real_payoff=participant_calculating_property['real_payoff'],
            )
            for participant_calculating_property in participant_calculating_properties
        ]
        return participant_calculating_properties, result

    def run(
        self,
        participant_attributes: dict[str, dict],
        network_effect: dict[str, float],
        price: dict,
        participant_choices: list[ParticipantChoice],
    ) -> Tuple[list[dict], list[ParticipantChoiceAndPayoff]]:
        """
        这个类的主要方法。
        输入participant的相关设置（默认必须，为了这个类尽可能无状态而以函数形式传递。），
        输入一轮中所有participant的选择，将其映射为计算完效用的相同长度的list。
        """
        return self.batch_get_participant_result(
            # participant_attributes={
            #     participant_id: participant_attribute.model_dump() for participant_id, participant_attribute in participant_attributes.items()
            # },
            participant_attributes=participant_attributes,
            network_effect=network_effect,
            price=price,
            participant_choices=[
                participant_choice.model_dump() for participant_choice in participant_choices
            ]
        )

