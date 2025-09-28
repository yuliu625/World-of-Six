from _experiments_history.configs.network_effects_with_prices import network_effects_with_prices_list
from _experiments_history.code.experiments.base_no_history_run import base_no_history_run

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
    await base_no_history_run(
        network_effects_with_prices_list,
        10,
        dir_to_save=r"D:\document\code\paper\World-of-Six\qwen_max_results/no_history_no_guidance",
        prompt_choice_dict=prompt_choice_dict,
        model_client=get_qwen(QwenModelName.qwen_max.value)
    )


if __name__ == '__main__':
    asyncio.run(main())
