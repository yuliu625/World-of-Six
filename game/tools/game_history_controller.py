from game.utils import JsonInputProcessor

import pandas as pd

import json


class GameHistoryController:
    """
    游戏历史的全部记录。
    utility_calculator通过participant的选择计算全部相关的计算属性，所有的结果都会保存在这里。
    使用这个类的标准化的方法提取需要的结果。
    """
    def __init__(
        self,
        init_columns: list[str] = None,
    ):
        self._columns = init_columns if init_columns is not None else [
            'game_round', 'participant_id',
            'standalone_value', 'network_effect', 'price',
            'expectation', 'expectation_payoff', 'is_participate',
            'real_participant_number', 'real_payoff',
        ]
        self.df = pd.DataFrame(
            columns=self._columns
        )

    def add_a_round_game_history(
        self,
        game_round: int,
        participant_round_calculating_properties: list[dict]
    ):
        """
        添加历史信息。
        轮数以一个字段值来记录。
        """
        for participant_calculating_property in participant_round_calculating_properties:
            self.df.loc[len(self.df)] = dict(
                game_round=game_round,
                **participant_calculating_property
            )

    def get_last_result(self, agent_id: str):
        history_record = self.df[self.df['participant_id'] == agent_id]
        return history_record.iloc[-1]

    def get_history_prompt(self, agent_id: str, game_round: int) -> str:
        """
        给一个具体的agent的history_prompt。
        Args:
            - agent_id: self.id.key
        """
        if game_round == 1:
            return ""
        history_record = self.df[self.df['participant_id'] == agent_id]
        # return history_record.to_dict(orient='records')
        # to_agent_history = history_record[
        #     ['game_round', 'price', 'expectation', 'real_participant_number']
        # ]
        real_participant_number_dict = history_record[['real_participant_number']].iloc[-1].to_dict()
        real_payoff_dict = history_record[['real_payoff']].iloc[-1].to_dict()
        real_participant_number_prompt = JsonInputProcessor.put_in_markdown(real_participant_number_dict)
        real_payoff_prompt = JsonInputProcessor.put_in_markdown(real_payoff_dict)
        # TODO: 加入template中
        return f"""在上一轮中，实际参与的人数为：\n{real_participant_number_prompt}\n因此，你实际获取的效用是：\n{real_payoff_prompt}\n"""

    def save_history(self, path_to_save):
        self.df.to_json(path_to_save, orient='records', lines=True, force_ascii=False)

