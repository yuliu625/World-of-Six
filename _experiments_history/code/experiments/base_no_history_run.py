from game.configs.participant_attributes import participant_attributes
from _experiments_history.configs.network_effects_with_prices import network_effects_with_prices_list

from game.prompts import BaseParticipantPromptFactory
from game import run_a_game

from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio


async def base_no_history_run(
    network_effects_with_prices_list: list[dict],
    repetition: int,
    dir_to_save: str,
    prompt_choice_dict: dict,
    model_client: OpenAIChatCompletionClient,
):
    for network_effect_index, network_effect_with_prices_list in enumerate(network_effects_with_prices_list):
        network_effect: dict = network_effect_with_prices_list['network_effect']
        prices_list: list[dict] = network_effect_with_prices_list['prices_list']
        print(network_effect)
        for price_index, price in enumerate(prices_list):
            print([price])
            for i in range(repetition):
                # print(rf"{dir_to_save}/network_effect_{network_effect_index}/price_{price_index}/{i}")
                await run_a_game(
                    game_round=1,
                    participant_attributes=participant_attributes,
                    network_effect=network_effect,
                    prices=[price],
                    dir_to_save=rf"{dir_to_save}/network_effect_{network_effect_index}/price_{price_index}/{i}",

                    model_client=model_client,
                    prompt_factory_class=BaseParticipantPromptFactory,

                    **prompt_choice_dict,
                )


if __name__ == '__main__':
    asyncio.run(base_no_history_run(network_effects_with_prices_list, 10, '/', 1, ))
