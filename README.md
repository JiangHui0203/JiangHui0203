<div align="center">

<img width="100%" src="./profile/banner.png" alt="Hui Jiang GitHub Profile Banner" />

<br/>

# Hui Jiang · 姜慧

**LLM Evaluation · Agent / Reasoning Systems · Applied LLM · Research Engineering**

**UCAS / CASIA M.S. (2027)** · **3+ years industry data experience** · **First-author research in LLM reasoning**

<a href="mailto:jianghui2024@ia.ac.cn">
  <img src="https://img.shields.io/badge/Email-jianghui2024%40ia.ac.cn-113F28?style=flat-square&logo=gmail&logoColor=white" alt="Email Hui Jiang" />
</a>
<a href="https://github.com/JiangHui0203">
  <img src="https://img.shields.io/badge/GitHub-@JiangHui0203-15803D?style=flat-square&logo=github" alt="GitHub profile" />
</a>

<br/><br/>

<code>Python</code> · <code>PyTorch</code> · <code>Transformers</code> · <code>SQL</code> · <code>LLM Evaluation</code> · <code>Experiment Design</code>

<br/><br/>

<strong>Open to 2027 graduate roles and research internships</strong><br/>
LLM Evaluation · Agent · Applied LLM · Research Engineer · Post-training / AI Data

</div>

---

## 20-second snapshot · 快速了解我

| | |
|---|---|
| **Research** | Adaptive test-time reasoning, reasoning evaluation, selective intervention |
| **Industry** | 3+ years of large-scale heterogeneous data analysis and delivery |
| **Research evidence** | First-author work on test-time reasoning and LLM mechanistic analysis |
| **Engineering** | Python, PyTorch, Transformers, SQL, Linux, Bash, Git, OpenPAI |
| **Target roles** | LLM Evaluation / Agent / Applied LLM / Research Engineer / AI Data |

我关注的核心问题是：

> **When should a model think more, where should additional test-time compute be spent, and when should we intervene?**

我的研究与工程经历可以概括为一条连续路径：

```text
Large-scale data & evaluation
          ↓
Understand model reasoning
          ↓
Evaluate reasoning states
          ↓
Allocate test-time compute
          ↓
Intervene selectively
```

---

## Portfolio map · 公开作品入口

如果你只有几分钟，可以按下面的顺序了解我的工作：

| Repository / Work | What it shows | Role in my profile |
|---|---|---|
| [**VeriAgent**](https://github.com/JiangHui0203/veriagent) | Verifiable Agent runtime, deterministic checks, recovery, structured traces, constrained Data Agent | **Agent / Research Engineering** |
| [**Homework**](https://github.com/JiangHui0203/Homework) | Agent knowledge system, LLM/Agent/Data knowledge base, pattern-oriented LeetCode Hot100 | **Systems thinking / Continuous learning** |
| [**NiceRice**](https://github.com/JiangHui0203/NiceRice) | Local-first WeChat Mini Program for real-world multi-constraint planning | **Product engineering / Side project** |
| **RoTFuse** *(private research repo)* | Low-confidence triggering, same-prefix exploration, candidate selection, compute-aware selective intervention | **Adaptive reasoning research** |

**Recommended recruiter path:** Profile → VeriAgent → Selected Research → Homework / NiceRice as supporting evidence.

---

## What I can bring · 我能带来的能力

### 1. LLM evaluation & reasoning analysis

能够从问题定义、baseline、数据切分、统计检验、计算成本到 failure analysis 搭建完整实验闭环，而不是只汇报单一 accuracy。

### 2. Research engineering

长期使用 **Python / PyTorch / Transformers / Linux / OpenPAI** 完成模型推理、日志采集、轨迹分析、实验调度与结果审计；关注可复现性、paired comparison 和 compute accounting。

公开工程项目 [**VeriAgent**](https://github.com/JiangHui0203/veriagent) 进一步展示了我对 Agent runtime 的工程理解：将 generation、verification、control 与 observability 分离，并在逻辑推理与结构化数据分析场景中保留可检查的执行证据。

### 3. Real-world data experience

研究生之前有三年多产业数据经验，长期处理百万至亿级多源异构数据，具备 SQL、数据治理、关系发现、规则策略、验证评估和业务交付经验。

### 4. Failure-oriented problem solving

研究中会保留负结果并追查原因。例如在 selective intervention 中，我会区分 candidate diversity、selector signal、semantic rescue 与 format / termination rescue，而不是只保留“成功案例”。

---

## Selected research · 代表研究

### More Thinking Is Not Always Better
**First Author · NLPCC 2026**

研究 test-time reasoning 中“更多思考是否一定更好”。结果表明，额外推理计算的收益并不单调，真正重要的是识别哪些实例值得更多计算，并避免无效或有害的 overthinking。

**Keywords:** Test-Time Reasoning · Adaptive Computation · Reasoning Evaluation  
[Paper](https://openreview.net/pdf?id=RigeZLi611)

### 大语言模型中的逻辑神经元
**第一作者 · 《软件学报》**

通过 gradient-based localization 与 inference-time intervention 分析逻辑推理相关功能单元，研究不同逻辑能力间的共享与任务特异组织，并验证局部干预对推理表现的影响。

**Keywords:** Mechanistic Interpretability · Logic Reasoning · Activation Intervention  
[Paper](https://www.jos.org.cn/josen/article/pdf/7704) · [DOI](https://doi.org/10.13328/j.cnki.jos.007704)

### RoTFuse · Research in Progress

进一步把问题推进到推理过程内部：在当前真实前缀下识别低置信推理单元，触发有限候选探索，并研究能否以受控额外计算实现局部修复。

当前重点包括：

- low-confidence triggering;
- same-prefix candidate generation;
- reasoning-state / local-value evaluation;
- selective intervention under explicit compute budgets;
- end-to-end correctness vs. additional inference cost;
- negative-result and selector-failure analysis.

**Research question:** *Can we identify where additional reasoning is actually worth paying for?*

---

## Industry experience · 产业经历

### 厦门市美亚柏科信息股份有限公司（北京分公司）
**Data Analyst · 2021.04 — 2024.08**

- 使用 **SQL** 处理百万至亿级多源异构数据，完成数据清洗、治理、分析与验证。
- 深度参与复杂关系发现、跨域身份数据融合与业务数据分析建模。
- 参与规则策略设计，并通过数据回放与指标验证持续修正方案。
- 覆盖需求拆解、数据建模、实验验证到最终交付的完整工作流。

这段经历让我在进入 LLM 研究后仍然保持一个很工程化的习惯：**先定义可验证问题，再构建数据与评测，最后讨论方法收益。**

---

## Systems & builds · 系统与实践

### [VeriAgent](https://github.com/JiangHui0203/veriagent)
**Verifiable Agent Runtime**

这是目前最能体现我 Agent / Research Engineering 能力的公开项目。项目包含两条相互独立但共享 verification-first 理念的 runtime：

- **ProofWriter VeriAgent**：面向多跳逻辑推理的 evidence retrieval、proof verification、controller-driven recovery 与 structured trace；
- **Olist Data Agent**：将 LLM 分析与 deterministic metric contract、read-only SQL、安全校验、cross-check 和 trace 结合起来的约束型数据分析 Agent。

**Relevant to:** Agent Evaluation · Runtime Control · Verification · Recovery · Observability · Data Agent

### [Homework · AI / Agent Knowledge & Interview Practice](https://github.com/JiangHui0203/Homework)

长期维护的个人知识与面试准备仓库。当前包括：

- Agent Knowledge System；
- LLM / Agent / Data Knowledge System；
- Pattern-oriented LeetCode Hot100，包括核心母题、模板库和专题解法。

它更接近一个持续维护的 **personal knowledge infrastructure**，而不是零散笔记集合。

### [NiceRice · 有时好饭](https://github.com/JiangHui0203/NiceRice)
**WeChat Mini Program · Side Project**

从真实生活约束出发的轻量工程实践，在日程、距离、天气、偏好与朋友时间之间寻找更合适的用餐安排，并采用 local-first 思路处理个人生活数据。

---

## Toolbox · 技术与方法

**LLM / Research**  
`PyTorch` · `Transformers` · `LLM Evaluation` · `Reasoning Analysis` · `Trajectory Analysis` · `Experiment Design` · `Statistical Testing`

**Engineering / Data**  
`Python` · `SQL` · `Linux` · `Bash` · `Git` · `OpenPAI` · `Data Processing`

**Research practice**  
rigorous baselines · paired comparisons · compute accounting · reproducible evaluation · failure analysis

---

## Education · 教育背景

- **中国科学院大学 · 人工智能学院 / 中国科学院自动化研究所** — *2024 — 2027*  
  硕士研究生 · LLM reasoning / evaluation / test-time computation

- **郑州轻工业大学 · 数学与应用数学** — *2017 — 2021*  
  理学学士 · 本科毕业论文获河南省优秀学士学位论文

---

## English snapshot

I am a Master's student at the **School of Artificial Intelligence, University of Chinese Academy of Sciences (UCAS)** / **Institute of Automation, Chinese Academy of Sciences (CASIA)**, with more than three years of prior industry experience in large-scale data analysis.

My current research centers on **adaptive test-time reasoning**: evaluating intermediate reasoning states, allocating inference-time compute, and selectively intervening when additional computation is likely to help.

I am particularly interested in roles around **LLM evaluation, Agent systems, applied LLMs, research engineering, and post-training / AI data**. My strengths lie in rigorous evaluation, experimental design, large-scale data work, reasoning analysis, and research-to-engineering execution.

For public engineering work, see [**VeriAgent**](https://github.com/JiangHui0203/veriagent). For my maintained Agent / LLM / Data knowledge systems and interview preparation, see [**Homework**](https://github.com/JiangHui0203/Homework).

---

## GitHub activity

<div align="center">

<a href="https://github.com/JiangHui0203">
  <img width="98%" src="./profile/activity.svg" alt="GitHub contribution activity" />
</a>

<br/><br/>

<a href="https://github.com/JiangHui0203">
  <img width="48.5%" src="./profile/stats.svg" alt="GitHub snapshot" />
</a>
<a href="https://github.com/JiangHui0203?tab=repositories">
  <img width="48.5%" src="./profile/top-langs.svg" alt="Top languages" />
</a>

</div>

---

<div align="center">

### when to think · where to think · when to stop

<sub>Reason carefully · Evaluate rigorously · Build things that work</sub>

</div>