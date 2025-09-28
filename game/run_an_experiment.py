from .run_a_game import run_a_game
from game.configs.participant_attributes import participant_attributes
from game.prompts import BaseParticipantPromptFactory

from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio


async def run_an_experiment(
    network_effect_with_prices_list: dict,
    repetition: int,
    dir_to_save: str,
    prompt_choice_dict: dict,
    model_client: OpenAIChatCompletionClient,
):
    network_effect: dict = network_effect_with_prices_list['network_effect']
    prices_list: list[dict] = network_effect_with_prices_list['prices_list']
    # print(network_effect)
    # print(prices_list)
    # return
    tasks = []
    for i in range(repetition):
        print(rf"{dir_to_save}/{i}")
        task = run_a_game(
            game_round=len(prices_list),
            participant_attributes=participant_attributes,
            network_effect=network_effect,
            prices=prices_list,
            dir_to_save=rf"{dir_to_save}/{i}",

            model_client=model_client,
            prompt_factory_class=BaseParticipantPromptFactory,

            **prompt_choice_dict,
        )
        tasks.append(task)
    await asyncio.gather(*tasks)
    await asyncio.sleep(120)

