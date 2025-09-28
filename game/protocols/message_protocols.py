"""
agent之间通讯的协议。
为适用autogen而定义。
"""

from dataclasses import dataclass
from pydantic import BaseModel


class GameSetting(BaseModel):
    system_prompt_template: str
    inference_prompt_template: str


class GameRequest(BaseModel):
    game_round: int
    # participant_message_template: str
    # history_prompt_template: str


class ManagerRequest(BaseModel):
    # system_prompt: str
    content: str
    # game_round: int


class ParticipantResponse(BaseModel):
    participant_id: str
    content: str
    result: dict
    # choice: str
    # analysis: str
    # expectation: str
    # reason: str


class ParsedResult(BaseModel):
    choice: bool
    analysis: str
    expectation: str
    reason: str

