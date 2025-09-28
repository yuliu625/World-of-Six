"""
LLM基础测试代码。
确认底层LLM有数学能力，并能够理解任务。
直接使用model client进行测试。
"""

from game import get_qwen, QwenModelName, ModelClientFactory, DeepseekModelName
from game.utils import load_prompt_template

from autogen_core.models import SystemMessage, UserMessage
from autogen_core import CancellationToken

import asyncio


async def test_prompt(model, system_prompt, inference_prompt):
    model = model
    result = await model.create(
        messages=[
            SystemMessage(
                content=system_prompt,
            ),
            UserMessage(
                content=inference_prompt,
                source='default'
            ),
        ],
        cancellation_token=CancellationToken()
    )
    print(result)
    return result


if __name__ == '__main__':
#     base_path = r"D:\document\code\paper\World-of-Six\game\prompts\test_prompts"
#     system_prompt_path = base_path + r"/system_prompt_1.txt"
#     inference_prompt_path = base_path + r"/inference_prompt_1.txt"
#     eg_system_prompt = load_prompt_template(system_prompt_path)
#     eg_inference_prompt = load_prompt_template(inference_prompt_path)
#
#     eg_model = get_qwen(QwenModelName.qwen_max.value)
#     asyncio.run(test_prompt(eg_model, eg_system_prompt, eg_inference_prompt))
#
# """
# finish_reason='stop' content='首先，我们根据提供的效用计算公式来分析这个问题。给定的条件是：\n\n- 你的独立收益（standalone_value）为1。\n- 网络边际收益（network_effect）为0.25。\n- 基础费用（price）为3。\n- 实际参与人数（participant_number）假设为3。\n\n代入这些值到效用公式中:\n\n\\[utility = standalone\\_value + network\\_effect \\times participant\\_number - price\\]\n\n将具体数值代入上述公式得到:\n\n\\[utility = 1 + 0.25 \\times 3 - 3\\]\n\n简化表达式:\n\n\\[utility = 1 + 0.75 - 3\\]\n\\[utility = 1.75 - 3\\]\n\\[utility = -1.25\\]\n\n因此，如果实际有3个人参加会议，你获得的效用将是-1.25。这意味着在这种情况下参加对你来说是不利的，因为你最终会损失1.25单位的价值。\n\n接下来，考虑如何基于这个信息预测参与人数以及决定自己是否参加。由于我的独立收益最低(1)，且价格相对较高(3)，除非预期网络效应能够显著提升总收益，否则我倾向于不参加。然而，考虑到其他参与者可能有不同的独立收益，并且可能会因为较高的独立收益或对更高参与人数的乐观预期而选择加入，这增加了复杂性。\n\n为了简化分析，我们可以设想一个情景：假设所有参与者都理性地估计参与人数并据此做出决策。对于那些拥有较高独立收益的人（比如5或6），即使在网络效应较低的情况下也可能愿意支付价格以换取潜在的好处。而对于像我这样独立收益较低的人来说，则需要更强烈的理由——即较高的预期参与人数来克服成本障碍。\n\n考虑到整个群体的独立收益分布和给定的价格，合理的预期可能是大约一半的人会选择参与（即3人左右）。但是，鉴于我个人的情况，除非我能确信会有足够多的人参加使得整体效用对我有利，否则我应该不会选择参加。\n\n综上所述，我的选择如下：\n```json\n{\n  "expectation": 3,\n  "reason": "基于独立收益的分布、给定的价格以及网络效应的影响，我认为最有可能的情况是有大约一半的参与者会选择加入会议。但由于我的独立收益较低，在当前设定下，除非预期参与人数远高于此，否则对我来说参加并不划算。"\n}\n```' usage=RequestUsage(prompt_tokens=449, completion_tokens=505) cached=False logprobs=None thought=None
# """

    eg_model = ModelClientFactory().get_deepseek()
    eg_system_prompt = '你是一个好帮手。'
    eg_inference_prompt = '9.11和9.8，哪个更大？'
    asyncio.run(test_prompt(eg_model, eg_system_prompt, eg_inference_prompt))

