from game.protocols import (
    ParticipantResponse
)

import pandas as pd


class ContextController:
    """
    上下文管理器。
    会记录所有的agent的响应。自动进行解析和管理。
    """
    def __init__(
        self,
        init_columns: list[str] = None,
    ):
        self._columns = init_columns if init_columns is not None else [
            'game_round', 'participant_id', 'content', 'expectation', 'reason'
        ]
        self.df = pd.DataFrame(
            columns=self._columns
        )

    def add_a_context(
        self,
        game_round: int,
        participant_round_context: ParticipantResponse
    ):
        """
        添加一条记录。
        Args:
            - game_round: 当前轮数是由manager进行管理的，因此需要额外传入。
            - participant_round_context: 直接的传入的agent的响应，需要额外处理。
        """
        new_context = dict(
            game_round=game_round,
            **self._parse_participant_response(participant_round_context)
        )
        # print(new_context)
        # 在末尾新增一条记录。
        self.df.loc[len(self.df)] = new_context

    def _parse_participant_response(self, participant_response: ParticipantResponse) -> dict:
        """
        解析响应协议。
        在修改协议时重构这个方法。
        主要为了处理嵌套结构。
        """
        participant_response = participant_response.model_dump()
        return dict(
            participant_id=participant_response['participant_id'],
            content=participant_response['content'],
            expectation=participant_response['result']['expectation'],
            reason=participant_response['result']['reason']
        )

    def save_context(self, path_to_save):
        self.df.to_json(path_to_save, orient='records', lines=True, force_ascii=False)

