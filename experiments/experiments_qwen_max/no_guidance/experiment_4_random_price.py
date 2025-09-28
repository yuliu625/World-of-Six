from game import run_an_experiment
from game.configs import PricesListFactory
from game import get_qwen, QwenModelName

from game.utils import load_prompt_template

import asyncio


def get_save_path(beta: float, price_index: int = 0):
    base_dir_to_save = r"D:\document\code\paper\World-of-Six\results\results_raw"
    dir_to_save_025 = base_dir_to_save + r"/beta_025/no_guidance"
    dir_to_save_075 = base_dir_to_save + r"/beta_075/no_guidance"
    if beta == 0.25:
        return dir_to_save_025 + rf"/random_price"
    elif beta == 0.75:
        return dir_to_save_075 + rf"/random_price"


def get_prompt_path_choice_dict(
    game_description_template_choice: int,
    standalone_value_distribution_prompt_template_choice: int,
    participant_attribute_prompt_template_choice: int,
    return_format_prompt_template_choice: int,
    inference_prompt_template_choice: int,
):
    base_path = r"/game/prompts/participant_prompts"
    system_prompts_path = base_path + r"/system_prompts"
    message_prompts_path = base_path + r"/message_prompts"

    return dict(
        game_description_template=rf"{system_prompts_path}/game_description_prompt_{game_description_template_choice}.txt",
        standalone_value_distribution_prompt_template=rf"{system_prompts_path}/standalone_value_prompt_{standalone_value_distribution_prompt_template_choice}.txt",
        participant_attribute_prompt_template=rf"{system_prompts_path}/participant_attribute_prompt_{participant_attribute_prompt_template_choice}.txt",
        return_format_prompt_template=rf"{system_prompts_path}/return_format_prompt_{return_format_prompt_template_choice}.txt",
        inference_prompt_template=rf"{message_prompts_path}/inference_prompt_{inference_prompt_template_choice}.txt"
    )


async def main(
    beta: float,
):
    prices_list_factory = PricesListFactory(beta)
    tasks = []
    network_effect_with_prices_list = prices_list_factory.get_random_price()
    await run_an_experiment(
        network_effect_with_prices_list=network_effect_with_prices_list,
        repetition=10,
        dir_to_save=get_save_path(beta),
        prompt_choice_dict=get_prompt_path_choice_dict(
            2,
            1,
            1,
            2,
            2
        ),
        model_client=get_qwen(QwenModelName.qwen_max.value)
    )
    #     tasks.append(task)
    # await asyncio.gather(*tasks)


if __name__ == '__main__':
    pass
    # asyncio.run(main(0.25))
    asyncio.run(main(0.75))
    # price_list_factory_025 = PricesListFactory(0.25)
    # price_list_factory_075 = PricesListFactory(0.75)
    # print(get_save_path(0.25, 1))
    # print(get_save_path(0.75, 2))
    # prompt_path_dict = get_prompt_path(
    #     2,
    #     1,
    #     1,
    #     2,
    #     2)
    # for _, path in prompt_path_dict.items():
    #     print(load_prompt_template(path))
