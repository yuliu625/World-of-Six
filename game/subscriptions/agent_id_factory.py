
from autogen_core import AgentId


class AgentIdFactory:
    def __init__(self, agent_attributes: dict, agent_type: dict):
        self.agent_attributes = agent_attributes
        self.agent_type = agent_type

    def get_agent_id(self, agent_type, agent_id_str) -> AgentId:
        return AgentId(type=agent_type, key=agent_id_str)

    def get_agent_ids(self):
        ...

