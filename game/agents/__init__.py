"""
定义各种agent，会在agent system中注册。
"""

__all__ = [
    'Manager',
    'Participant',
    'SmartParticipant',
    'DumbParticipant',
]

from .manager import Manager
from .participant import Participant
from .smart_participant import SmartParticipant
from .dumb_participant import DumbParticipant
