"""
participant后续会接收到的信息。
为了复用性，由manager管理，当然最终统一由prompt factory生成。
包含:
    - history_prompt: 过去的选择。用于多轮对话。
    - round_prices_prompt: 变量，每轮给出的价格，即price。
    - inference_prompt: 引导agent进行推理。主要为CoT各种模板。
"""
