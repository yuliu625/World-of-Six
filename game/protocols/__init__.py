"""
数据类。
为符合autogen使用。为方便我构建工程。
"""

from .message_protocols import (
    GameSetting,
    GameRequest,
    ManagerRequest,
    ParticipantResponse,
    ParsedResult
)

from .participant_protocols import (
    ParticipantConfig,
    ParticipantAttribute,
    ParticipantStructuredOutput,
    ParticipantChoice,
    ParticipantChoiceAndPayoff,
)

