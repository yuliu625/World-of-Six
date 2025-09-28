# Communication Design


## Overview
每个Agent并不是所有的信息都需要接收，这是multi-agent的两个优势之一。

复杂的agent system需要一个类似planning或manager的角色。但是在博弈论的实验中，这是不需要的。这里，需要的是可以进行可靠的计算和规范调度其他agent的中央agent，可以并应该由完全的程序算法实现。

实验或许不能一轮就能够到达最终的均衡，多轮实验不断迭代可以直接实现并且看起来会是更好的选择。


## Workflow
### Config
- 控制者
  1. 控制所有的信息，但仅向每个agent给出必要的信息。
- 参与者
  1. 不能知道其他agent的本轮选择。
  2. 可以知道所有agent的历史选择。
  3. 每轮仅可做出选择。（可以给出推理过程。）

### Realization
- 控制者（程序实现）
  1. 进行实验。调用其他agent。
     - 相同的。引导的prompt、所有agent的历史选择。
     - 不同的。对应agent的编号。
  2. 统计并计算结果。
     - 通讯和选择要求以JSON格式给出。正则化方式提取选择。
     - 由确定的程序计算结果。

- 参与者（LLM实现）
  1. 返回结果以JSON格式给出。
  2. 每次做出选择是知道自己的id的。
  3. 需要展现思考和预期。

### Message Protocol
这里用3种协议就可以进行控制。


## Algorithm
```
Manager: 设置每个agent
for-loop:
    Manager: 让每个agent做出选择
    for-loop:
        Agent: 分析，做出选择，返回
    Manager: 统计结果，记录
    Manager: 计算
Manager: 返回迭代的结果
```
