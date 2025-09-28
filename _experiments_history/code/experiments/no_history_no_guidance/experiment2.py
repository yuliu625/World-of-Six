"""
未计算理论解，使用初始的prompt。
"""

from game.configs.participant_attributes import participant_attributes
from _experiments_history.configs.network_effects import network_effect_1
from _experiments_history.configs.prices import prices_1

from game.prompts import BaseParticipantPromptFactory
from game import run_a_game, get_qwen, QwenModelName

import asyncio


async def main():
    for price_index in range(6):
        for i in range(10):
            await run_a_game(
                game_round=1,
                participant_attributes=participant_attributes,
                network_effect=network_effect_1,
                prices=[prices_1[price_index]],
                dir_to_save=rf"/results/baseline_demo/network_effect_1/price{price_index}/{i}",

                model_client=get_qwen(QwenModelName.qwen_15.value),
                prompt_factory_class=BaseParticipantPromptFactory,

                **dict(
                    game_description_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\game_description_prompt_1",
                    standalone_value_distribution_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\standalone_value_prompt_1",
                    participant_attribute_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\participant_attribute_prompt_1",
                    return_format_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\return_format_prompt_1",
                    inference_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\message_prompts\inference_prompt_1"
                )
            )


if __name__ == '__main__':
    asyncio.run(main())
