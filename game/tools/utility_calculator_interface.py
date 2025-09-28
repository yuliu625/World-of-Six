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

from typing import Callable


class BaseUtilityCalculator:
    def __init__(
        self, calculate_utility_func: Callable
    ):
        """
        为了尽可能无状态，计算器仅与效用计算方法绑定。
        Args:
            - calculate_utility_func: 效用计算函数。需要以kwargs形式传递参数，命名需要一致。
        """
        self.calculate_utility_func = calculate_utility_func

    def get_choices_list(self, participant_choices: list[ParticipantChoice]) -> list[bool]:
        """
        这个方法可能在不同输出的情况下被重写。
        仅为了计算参与人数，不是为了得到确定的映射关系。
        """
        return [participant_choice.choice for participant_choice in participant_choices]
        # result = []
        # for participant_choice in participant_choices:
        #     if participant_choice.choice == 'True':
        #         result.append(True)
        #     else:
        #         result.append(False)
        # return result

    def calculate_participant_number_by_choices_list(self, choices: list[bool]) -> int:
        """
        当参与情况以bool方式表示时的计算方法。
        """
        return sum(choices)

    def get_participant_number(self, participant_choices: list[ParticipantChoice]) -> int:
        """
        计算参与人数的方法。

        默认，participant agent进行数据校验和重新请求，确保choice字段为bool。
        """
        choices_list = self.get_choices_list(participant_choices)
        participant_number = self.calculate_participant_number_by_choices_list(choices_list)
        return participant_number

    def calculate_utility(
        self,
        participant_number: int,
        participant_attribute,
        is_participate: bool
    ) -> float:
        """
        计算一个participant选择的收益。

        需要这个participant的计算相关属性。
        """
        if is_participate:
            return self.calculate_utility_func(
                standalone_value=participant_attribute.standalone_value,
                network_benefit=participant_attribute.network_benefit,
                participant_number=participant_number,
                price=10
            )
        else:
            return 0

    def get_participant_result(
        self,
        participant_number: int,
        participant_attribute: ParticipantAttribute,
        participant_choice: ParticipantChoice,
    ) -> ParticipantChoiceAndPayoff:
        """
        计算一个participant的结果。

        这里会涉及dataclass的转换，有可能重写。

        Args:
            - participant_number: 参与人数。
            - participant_attribute: 一个participant的计算属性。
            - participant_choice: 一个participant的选择。
        """
        participant_utility = self.calculate_utility(
            participant_number=participant_number,
            participant_attribute=participant_attribute,
            is_participate=participant_choice.choice
        )
        return ParticipantChoiceAndPayoff(
            participant_id=participant_choice.participant_id,
            choice=participant_choice.choice,
            payoff=participant_utility,
        )

    def batch_get_participant_result(
        self,
        participant_attributes: dict[str, ParticipantAttribute],
        participant_choices: list[ParticipantChoice],
    ) -> list[ParticipantChoiceAndPayoff]:
        """
        计算一组participant的效用，映射2种dataclass。
        Args:
            - participant_attributes: 所有participant的计算属性。
            - participant_choices: 所有participant的选择。
        """
        participant_number = self.get_participant_number(participant_choices)
        result = []
        for participant_choice in participant_choices:
            participant_attribute = participant_attributes[participant_choice.participant_id]
            participant_result = self.get_participant_result(
                participant_number=participant_number,
                participant_attribute=participant_attribute,
                participant_choice=participant_choice,
            )
            result.append(participant_result)
        return result

    def run(
        self,
        participant_attributes: dict[str, ParticipantAttribute],
        participant_choices: list[ParticipantChoice],
    ) -> list[ParticipantChoiceAndPayoff]:
        """
        这个类的主要方法。
        输入participant的相关设置（默认必须，为了这个类尽可能无状态而以函数形式传递。），
        输入一轮中所有participant的选择，将其映射为计算完效用的相同长度的list。
        """
        return self.batch_get_participant_result(
            participant_attributes=participant_attributes,
            participant_choices=participant_choices
        )

