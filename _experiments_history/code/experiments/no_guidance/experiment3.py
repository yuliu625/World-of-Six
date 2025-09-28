from game.configs.participant_attributes import participant_attributes
from _experiments_history.configs.network_effects_with_prices import network_effects_with_prices_list_1, network_effects_with_prices_list_2

from game.prompts import BaseParticipantPromptFactory
from game import run_a_game, get_qwen, QwenModelName

import asyncio


async def base_run(
    network_effect_with_prices_list: dict,
    repetition: int,
    dir_to_save: str,
    prompt_choice_dict: dict,
):
    network_effect: dict = network_effect_with_prices_list['network_effect']
    prices_list: list[dict] = network_effect_with_prices_list['prices_list']
    print(network_effect)
    prices_list.reverse()
    for i in range(repetition):
        print(rf"{dir_to_save}/{i}")
        await run_a_game(
            game_round=len(prices_list),
            participant_attributes=participant_attributes,
            network_effect=network_effect,
            prices=prices_list,
            dir_to_save=rf"{dir_to_save}/{i}",

            model_client=get_qwen(QwenModelName.qwen_15.value),
            prompt_factory_class=BaseParticipantPromptFactory,

            **prompt_choice_dict,
        )


async def main():
    prompt_choice_dict = dict(
        game_description_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\game_description_prompt_2.txt",
        standalone_value_distribution_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\standalone_value_prompt_1.txt",
        participant_attribute_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\participant_attribute_prompt_1.txt",
        return_format_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\return_format_prompt_2.txt",
        inference_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\message_prompts\inference_prompt_2.txt"
    )
    for i, network_effect_with_prices_list in enumerate(network_effects_with_prices_list_1):
        await base_run(
            network_effect_with_prices_list,
            10,
            dir_to_save=r"/_experiments_history/results_raw/no_guidance/network_effect_1/reverse_order_price",
            prompt_choice_dict=prompt_choice_dict,
        )
    for i, network_effect_with_prices_list in enumerate(network_effects_with_prices_list_2):
        await base_run(
            network_effect_with_prices_list,
            10,
            dir_to_save=r"/_experiments_history/results_raw/no_guidance/network_effect_2/reverse_order_price",
            prompt_choice_dict=prompt_choice_dict,
        )


if __name__ == '__main__':
    asyncio.run(main())
