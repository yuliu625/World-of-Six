"""
根据设置，运行一次试验。
"""

from game.runtime import GameRunner
from game.protocols import ParticipantStructuredOutput, GameRequest
from game.tools import calculate_utility
from game.prompts import BaseParticipantPromptFactory

from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio


async def base_run_a_game(
    manager_config,
    participant_config,
    game_request
):
    """
    运行实验。
    设置相关的内容需要到configs中进行修改。
    """
    game_runner = GameRunner(
        manager_config=manager_config,
        participant_config=participant_config,
    )

    await game_runner.run_a_game(
        game_request
    )


def get_game_request(game_round: int):
    return GameRequest(
        game_round=game_round
    )


def get_participant_config(
    model_client,
    prompt_factory
):
    return dict(
        description='实验的参与者。',
        model_client=model_client,
        structured_output_format=ParticipantStructuredOutput,
        prompt_factory=prompt_factory,
        config=None,
    )


def get_manager_config(
    participant_attributes: dict[str, dict],
    network_effect: dict[str, float],
    prices: list[dict],
    prompt_factory: BaseParticipantPromptFactory,
    # prompt_factory_class: type[BaseParticipantPromptFactory],
    prompt_template_config: dict,
    dir_to_save: str,
):
    return dict(
        description='实验的控制者。',
        participant_attributes=participant_attributes,
        network_effect=network_effect,
        prices=prices,
        calculate_utility_func=calculate_utility,
        prompt_factory=prompt_factory,
        # prompt_factory_class=prompt_factory_class,
        config=dict(
            prompt_template_config=prompt_template_config,
            dir_to_save=dir_to_save,
        )
    )


def get_prompt_factory(
    prompt_factory_class,
    participant_attributes: dict[str, dict] = None,
    network_effect: dict = None,
    prices: list[dict] = None,
    prompt_template_config: dict = None,
):
    return prompt_factory_class(
        participant_attributes=participant_attributes,
        network_effect=network_effect,
        round_prices=prices,
        prompt_template_config=prompt_template_config,
    )


def get_prompt_template_config(
    game_description_template: str = None,
    standalone_value_distribution_prompt_template: str = None,
    participant_attribute_prompt_template: str = None,
    return_format_prompt_template: str = None,
    inference_prompt_template: str = None,
) -> dict:
    """选择template指定的是path。"""
    return dict(
        game_description_template=game_description_template,
        standalone_value_distribution_prompt_template=standalone_value_distribution_prompt_template,
        participant_attribute_prompt_template=participant_attribute_prompt_template,
        return_format_prompt_template=return_format_prompt_template,
        inference_prompt_template=inference_prompt_template,
    )


async def run_a_game(
    game_round: int,

    participant_attributes: dict[str, dict],
    network_effect: dict[str, float],
    prices: list[dict],
    dir_to_save: str,

    model_client: OpenAIChatCompletionClient,
    prompt_factory_class: type[BaseParticipantPromptFactory] = BaseParticipantPromptFactory,

    game_description_template: str = None,
    standalone_value_distribution_prompt_template: str = None,
    participant_attribute_prompt_template: str = None,
    return_format_prompt_template: str = None,
    inference_prompt_template: str = None,
):
    """组合完成所有的设置。避免重复构建设置。"""
    prompt_template_config = get_prompt_template_config(
        game_description_template=game_description_template,
        standalone_value_distribution_prompt_template=standalone_value_distribution_prompt_template,
        participant_attribute_prompt_template=participant_attribute_prompt_template,
        return_format_prompt_template=return_format_prompt_template,
        inference_prompt_template=inference_prompt_template,
    )
    prompt_factory = get_prompt_factory(
        prompt_factory_class=prompt_factory_class,
        participant_attributes=participant_attributes,
        network_effect=network_effect,
        prices=prices,
        prompt_template_config=prompt_template_config,
    )
    manager_config = get_manager_config(
        participant_attributes=participant_attributes,
        network_effect=network_effect,
        prices=prices,
        prompt_factory=prompt_factory,
        prompt_template_config=prompt_template_config,
        dir_to_save=dir_to_save,
    )
    participant_config = get_participant_config(
        model_client=model_client,
        prompt_factory=prompt_factory,
    )
    game_request = get_game_request(game_round=game_round)
    await base_run_a_game(
        manager_config=manager_config,
        participant_config=participant_config,
        game_request=game_request,
    )

