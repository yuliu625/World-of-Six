from game.configs.participant_attributes import participant_attributes
from _experiments_history.configs.network_effects_with_prices import network_effects_with_prices_list

from game.prompts import BaseParticipantPromptFactory
from game import run_a_game

from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio


async def base_with_history_run(
    network_effect_with_prices_list: dict,
    repetition: int,
    dir_to_save: str,
    prompt_choice_dict: dict,
    model_client: OpenAIChatCompletionClient,
):
    network_effect: dict = network_effect_with_prices_list['network_effect']
    prices_list: list[dict] = network_effect_with_prices_list['prices_list']
    print(network_effect)
    for i in range(repetition):
        print(rf"{dir_to_save}/{i}")
        await run_a_game(
            game_round=len(prices_list),
            participant_attributes=participant_attributes,
            network_effect=network_effect,
            prices=prices_list,
            dir_to_save=rf"{dir_to_save}/{i}",

            model_client=model_client,
            prompt_factory_class=BaseParticipantPromptFactory,

            **prompt_choice_dict,
        )


if __name__ == '__main__':
    asyncio.run(base_with_history_run(network_effects_with_prices_list[0], 10, '/', 1, ))
