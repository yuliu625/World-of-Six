from _experiments_history.configs.network_effects_with_prices import network_effects_with_prices_list_1, network_effects_with_prices_list_2
from _experiments_history.code.experiments.base_with_history_run import base_with_history_run

import asyncio


async def main():
    prompt_choice_dict = dict(
        game_description_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\game_description_prompt_2.txt",
        standalone_value_distribution_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\standalone_value_prompt_1.txt",
        participant_attribute_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\participant_attribute_prompt_1.txt",
        return_format_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\return_format_prompt_2.txt",
        inference_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\message_prompts\inference_prompt_2.txt"
    )
    for i, network_effect_with_prices_list in enumerate(network_effects_with_prices_list_1):
        await base_with_history_run(
            network_effect_with_prices_list,
            10,
            dir_to_save=r"/_experiments_history/results_raw/no_guidance/network_effect_1/sequence_price",
            prompt_choice_dict=prompt_choice_dict,
        )
    for i, network_effect_with_prices_list in enumerate(network_effects_with_prices_list_2):
        await base_with_history_run(
            network_effect_with_prices_list,
            10,
            dir_to_save=r"/_experiments_history/results_raw/no_guidance/network_effect_2/sequence_price",
            prompt_choice_dict=prompt_choice_dict,
        )


if __name__ == '__main__':
    asyncio.run(main())
