from _experiments_history.code.experiments.repeating_prices import network_effects_with_prices_list_1, network_effects_with_prices_list_2
from _experiments_history.code.experiments.base_with_history_run import base_with_history_run

from game import get_qwen, QwenModelName

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
            1,
            dir_to_save=rf"D:\document\code\paper\World-of-Six\results/no_guidance/network_effect_1/same_price/{i}",
            prompt_choice_dict=prompt_choice_dict,
            model_client=get_qwen(QwenModelName.qwen_15.value),
        )
    for i, network_effect_with_prices_list in enumerate(network_effects_with_prices_list_2):
        await base_with_history_run(
            network_effect_with_prices_list,
            1,
            dir_to_save=rf"D:\document\code\paper\World-of-Six\results/no_guidance/network_effect_2/same_price{i}",
            prompt_choice_dict=prompt_choice_dict,
            model_client=get_qwen(QwenModelName.qwen_15.value),
        )


if __name__ == '__main__':
    asyncio.run(main())
