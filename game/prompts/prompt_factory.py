
from game.utils import (
    JsonInputProcessor,
    load_prompt_template,
)


class BaseParticipantPromptFactory:
    def __init__(
        self,
        participant_attributes: dict,
        network_effect: dict,
        round_prices: list[dict],
        prompt_template_config: dict,
    ):
        self.participant_attributes = participant_attributes
        self.network_effect = network_effect
        self.round_prices = round_prices
        self.prompt_template_config = prompt_template_config

    def get_system_prompt(self, agent_id: str) -> str:
        # 获取设置信息。
        standalone_value_distribution_str = JsonInputProcessor.put_in_markdown(
            [participant_attribute['standalone_value'] for _, participant_attribute in self.participant_attributes.items()],
        )
        network_effect_str = JsonInputProcessor.put_in_markdown(self.network_effect)
        participant_attribute_str = JsonInputProcessor.put_in_markdown(self.participant_attributes[agent_id])

        # 模板填写。
        game_description = load_prompt_template(
            self.prompt_template_config['game_description_template']
        )
        standalone_value_distribution_prompt = load_prompt_template(
            self.prompt_template_config['standalone_value_distribution_prompt_template']
        ).format(standalone_value_distribution=standalone_value_distribution_str)
        participant_attribute_prompt = load_prompt_template(
            self.prompt_template_config['participant_attribute_prompt_template']
        ).format(network_effect=network_effect_str, participant_attribute=participant_attribute_str)
        return_format_prompt = load_prompt_template(
            self.prompt_template_config['return_format_prompt_template']
        )
        return f"{game_description}\n{standalone_value_distribution_prompt}\n{participant_attribute_prompt}\n{return_format_prompt}"

    def get_inference_prompt(self, game_round: int) -> str:
        round_price_dict = self.round_prices[game_round]
        round_price_str = JsonInputProcessor.put_in_markdown(round_price_dict)

        inference_prompt_template = load_prompt_template(
            self.prompt_template_config['inference_prompt_template']
        )
        return inference_prompt_template.format(round_price_str=round_price_str)

    def get_history_prompt(self, agent_id: str, game_round: int) -> str:
        """这个或许可以由game_history_controller来实现。"""
        if game_round == 1:
            return ""
        # history_prompt_template = load_prompt_template(
        #     self.prompt_template_config['history_prompt_template']
        # )
        return ""

