"""
qwen15
beta=0.25, 0.75
没有历史信息，但是使用引导。
"""

from game.configs.participant_attributes import participant_attributes
from _experiments_history.configs.network_effects import network_effect_1, network_effect_2
from _experiments_history.configs.prices import prices_1, prices_2

from game.prompts import BaseParticipantPromptFactory
from game import run_a_game, get_qwen, QwenModelName

import asyncio


async def main():
    for price_index in range(len(prices_1)):
        for i in range(10):
            await run_a_game(
                game_round=1,
                participant_attributes=participant_attributes,
                network_effect=network_effect_1,
                prices=[prices_1[price_index]],
                dir_to_save=rf"D:\document\code\paper\World-of-Six\results\no_history/network_effect_1/price_{price_index}/{i}",

                model_client=get_qwen(QwenModelName.qwen_15.value),
                prompt_factory_class=BaseParticipantPromptFactory,

                **dict(
                    game_description_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\game_description_prompt_2.txt",
                    standalone_value_distribution_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\standalone_value_prompt_1.txt",
                    participant_attribute_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\participant_attribute_prompt_1.txt",
                    return_format_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\return_format_prompt_3.txt",
                    inference_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\message_prompts\inference_prompt_4.txt"
                )
            )

    for price_index in range(len(prices_2)):
        for i in range(10):
            await run_a_game(
                game_round=1,
                participant_attributes=participant_attributes,
                network_effect=network_effect_2,
                prices=[prices_2[price_index]],
                dir_to_save=rf"D:\document\code\paper\World-of-Six\results\no_history/network_effect_2/price_{price_index}/{i}",

                model_client=get_qwen(QwenModelName.qwen_15.value),
                prompt_factory_class=BaseParticipantPromptFactory,

                **dict(
                    game_description_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\game_description_prompt_2.txt",
                    standalone_value_distribution_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\standalone_value_prompt_1.txt",
                    participant_attribute_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\participant_attribute_prompt_1.txt",
                    return_format_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\system_prompts\return_format_prompt_3.txt",
                    inference_prompt_template=r"D:\document\code\paper\World-of-Six\game\prompts\participant_prompts\message_prompts\inference_prompt_4.txt"
                )
            )


if __name__ == '__main__':
    asyncio.run(main())
