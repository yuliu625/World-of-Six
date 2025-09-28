"""
我为了处理participant各种复杂配置而定义的数据类。
部分实际符合，但被弃用。
"""

from pydantic import BaseModel


class ParticipantConfig(BaseModel):
    system_prompt_template: str


class ParticipantAttribute(BaseModel):
    participant_id: str
    standalone_value: float
    # network_benefit: float
    # price: float


participant_attributes: dict[str, ParticipantAttribute]


class RoundGameSetting(BaseModel):
    network_benefit: float
    price: float


class ParticipantChoice(BaseModel):
    participant_id: str
    expectation: int


class ParticipantStructuredOutput(BaseModel):
    expectation: int
    reason: str


class ParticipantChoiceAndPayoff(BaseModel):
    participant_id: str
    expectation: int
    expectation_payoff: float
    is_participate: bool
    real_participant_number: int
    real_payoff: float


game_history: list[ParticipantChoiceAndPayoff]

