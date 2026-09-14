<div align="center">

# Hui Jiang 👋

### 大模型推理 · Test-Time Reasoning · LLM Evaluation

研究与实践聚焦 **大语言模型推理、测试时计算与推理评测**，  
关注模型何时需要更多推理、推理资源应该如何分配，以及如何评估中间推理状态。

<br/>

**第一作者论文《软件学报》录用 · RoTFuse 开源项目 · LLM 推理与评测**

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-JiangHui0203-181717?style=flat-square&logo=github)](https://github.com/JiangHui0203)
[![English](https://img.shields.io/badge/English-README_EN.md-0A66C2?style=flat-square)](./README_EN.md)

</div>

---

## ✨ 亮点速览

- 📄 **第一作者论文被《软件学报》录用**，研究大语言模型中的逻辑神经元定位与干预
- 🧠 系统研究 **Test-Time Reasoning / 推理深度 / 自适应计算分配**
- 🧩 开发 **RoTFuse**，探索推理过程中的 local state evaluation 与 inference-time intervention
- 🔬 具备从 **研究问题 → 实验设计 → 模型运行 → 统计检验 → 失败审计 → 结论边界** 的完整实验经验
- ⚙️ 长期使用 PyTorch / Transformers / GPU 集群开展 LLM inference 与 evaluation 实验

---

## 👋 关于我

目前在 **中国科学院大学人工智能学院 / 中国科学院自动化研究所** 开展大语言模型相关研究。

主要关注：

- 大模型推理（LLM Reasoning）
- 测试时计算（Test-Time Computation）
- 推理评测与干预（Reasoning Evaluation & Intervention）
- 逻辑推理（Logical Reasoning）
- 模型内部机制与可解释性（Mechanistic Interpretability）

我比较关心一个贯穿这些工作的核心问题：

> **额外推理什么时候真正有价值，我们能否在推理过程中提前判断？**

相比单纯增加 reasoning tokens，我更关注如何建立可测量、可复现的实验体系，判断额外计算究竟是在推进推理，还是只是在增加成本。

---

## 🚀 代表工作

### 🧠 More Thinking Is Not Always Better

**面向逻辑推理的 Test-Time Computation 与自适应计算分配**

围绕“模型是否想得越久越好”这一问题，对不同 test-time reasoning 策略进行了系统比较。

**我做了什么**

- 在 **ProofWriter、PrOntoQA、ProverQA、FOLIO** 4 个逻辑推理数据集上开展实验
- 比较 no-thinking、native reasoning、fixed-depth reasoning 与 adaptive reasoning 等策略
- 从 **结构性负荷（structural load）** 与 **语义不稳定性（semantic instability）** 两个维度分析问题难度
- 使用 bootstrap、McNemar test 等方法验证实验差异
- 设计自适应推理与 routing / auditing 实验

**主要发现**

- 推理深度与准确率并非简单单调关系
- 在部分设置中，继续增加 reasoning depth 反而降低准确率
- 不同问题对 test-time computation 的需求存在明显差异
- 推理预算的合理分配比统一增加推理长度更重要

**我的角色**

`第一作者 · 方法设计 · 实验实现 · 数据分析 · 论文撰写`

---

### 🔬 大语言模型中的逻辑神经元

**逻辑推理相关神经元的定位、干预与迁移分析**

📄 **第一作者 · 《软件学报》录用**

研究模型内部是否存在与逻辑推理行为稳定相关的神经组件。

**我做了什么**

- 基于 loss-gradient sensitivity 定位 logic-related neurons
- 在 LogicBench 多类逻辑任务上进行系统实验
- 使用 inference-time activation scaling 对目标神经元进行增强 / 抑制
- 设置随机神经元与非逻辑神经元作为对照
- 分析不同层、不同逻辑任务之间的 shared / specific representation

**实验观察**

- 定位后的神经元干预明显强于随机与非逻辑对照
- 抑制目标神经元产生更明显的性能变化
- logic-related neurons 在模型中层出现较明显富集
- 不同逻辑任务之间同时存在共享和任务特异的内部组件

**我的角色**

`第一作者 · 方法设计 · 模型实验 · 干预分析 · 论文撰写`

---

### 🧩 [RoTFuse](https://github.com/JiangHui0203/RoTFuse)

**Test-Time Reasoning 中的局部推理状态评估与干预**

RoTFuse 研究的问题是：

> 当模型已经生成到某个中间 reasoning state 时，
> 能否判断哪一个方向更值得继续？

当前框架围绕：

```text
reasoning prefix P
        ↓
provisional state u₀
        ↓
optional sibling candidates
        ↓
local state evaluation
        ↓
replace / abstain
        ↓
continue reasoning
