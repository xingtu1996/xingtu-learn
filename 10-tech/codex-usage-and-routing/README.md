# ChatGPT Chat、Work 与 Codex：模型、Token 与额度边界

> **status：活跃｜类型：技术学习 / 可复用工作方法｜首次核验：2026-10-30**  
> 本文是会变化的**产品知识**，不是永久定价表。套餐、模型名称和限额以官方当日页面与实际账户展示为准。

## 读者能拿走什么
一套简单的选择方法：先判断问题是“讨论、跨应用交付还是工程执行”，再看使用哪种额度、什么模型、怎样记录证据，避免把每个任务都丢给高成本 Agent。

## 一、先厘清三个经常被混用的概念

| 概念 | 含义 | 不应该混为 |
|---|---|---|
| Token | 模型处理输入/输出等内容的计量单位 | 不等于一次消息，也不等于美元费用 |
| 使用额度 / Allowance | 产品套餐限定的可用量，可能有时窗 | 不等于固定的 Token 总量或可执行任务次数 |
| Credits / API 费用 | 在适用条件下的扩展额度或独立 API 计费 | 不等于 ChatGPT 普通聊天套餐免费无限执行 |

**普通 ChatGPT 聊天会消耗模型计算，但其聊天使用限制与 Work/Codex 共享的 Agent 执行额度是不同的机制。** “不扣 Work/Codex 额度”不是“没有 Token 消耗”，也不是“Chat 绝对不限量”。

## 二、哪个产品做什么

| 工作方式 | 典型任务 | 限额理解 |
|---|---|---|
| Chat（普通聊天） | 解释概念、设计 SDD、计划、写提示词、审查方案、使用允许的连接器查询/操作 | 受 Chat 的模型/工具等独立限制约束 |
| Work | 多步研究、跨网页/应用操作、交付较大的工作产物 | 与 Codex 共用适用套餐的 Work/Codex allowance |
| Codex Local / CLI | 修改代码、文件、运行本地命令与测试 | 以登录方式与配置决定所属套餐/计费；用 ChatGPT 登录时适用 Codex allowance |
| Codex Cloud | 云端仓库工程任务 | 使用适用的共享额度；复杂云任务可能消耗更高 |
| OpenAI API Key | 自己的 API 集成与调用 | **单独按 API 规则计费**，不能当作 ChatGPT 订阅额度 |

对于具体模型，Work/Codex 中的 `Default` 是产品的默认模型与思考档位组合；可选的具体模型和推理强度随套餐、工作空间与版本变化。**不要把“我这次看到 Default”写成某个永远固定的底层型号。**

## 三、行途式低浪费工作流

1. **Chat 先定需求**：范围、输入来源、优先级、非目标、验收标准。
2. **GitHub 管版本与证据**：尽量通过 Issue/分支/Draft PR 完成可审阅的文档与结构调整；对私有 Raw 不主动同步。
3. **Codex / Work 做确需执行的事情**：本地工程、运行验证、实际浏览器与跨应用操作。
4. **人做最终判断**：例如公众号选题与文章群发不授权 Agent 默默替代。
5. **用结果衡量效率**：关注“每次通过验收的交付所需资源”，而不是简单把 Token 下降当成功。

### 示例：公众号明日选题
- Chat 可分析 GitHub 上已存在的发布包、历史选题和 SSoT，并提交 Draft PR 的决策说明。
- Codex Local / Work 用于未提交的本地素材、CLI Skill、公众号后台或视觉预览。
- 最终发布必须以人工审核和实际后台状态为准；GitHub 上“已建草稿”的记录不是实时凭证。

## 四、如何观察额度与计算效率

**先看官方套餐剩余量和重置时间，再结合实际任务日志。**

- Codex 交互内可用 `/status` 查看状态（界面与版本可能不同）。
- ChatGPT Desktop 的 Settings / Usage 或 Usage & billing 页面可查看适用账号的额度与历史。
- 任务级记录：任务 ID、模型、推理强度、工具、Skill、文件、执行次数、失败重试、验收结论。
- 若可从可信接口取得输入/输出/缓存 Token、额度前后快照则记录；取不到用“未知”而非补数字。
- 不把一次任务的模型 Token 精确等同于五小时或每周额度百分比。

## 五、容易踩的坑

1. 误把普通 Chat 视为“没有 Token 消耗”。
2. 将 Codex Desktop 内的 Quick Chat 当作无成本的普通 Chat 聊天。
3. 不查当前模型菜单，将 Default 和具体模型永久绑定。
4. 把本地已忽略的原始素材直接推 GitHub，导致隐私风险。
5. 只统计工具调用次数、不结合质量和失败重试看投入产出。
6. 把“GitHub 已提交”“后台已建稿”“已经发布”误认为同一个状态。

## 六、可复用检查单

- [ ] 任务能否先在 Chat 澄清并形成明确任务包？
- [ ] 是否已有成熟稿、已有脚本或可复用 Skill？
- [ ] 是否真的需要本地命令、浏览器或跨应用执行？
- [ ] 本次 Work/Codex 可用额度、窗口和模型强度是什么？
- [ ] 是否有可验证产物、隐私门禁、回滚路径和人工审批点？
- [ ] 有无复用资产、失败重试或无效上下文导致的浪费？

## 七、官方资料与维护

- [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) — 两种工作模式、模型和共享额度。
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) — 登录、限制、状态查看。
- [Managing usage with GPT-6 Astra in Work and Codex](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) — 额度窗口、模型消耗差异。
- [GPT-6 and other models in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt) — Chat 模型与自身限制。

**维护方式：** 当官方模型/额度规则变化时，标注核验日期和变更点；不要覆盖旧结论来源。本页以通用原则为主，实时数字以账户 Usage 页面为准。

## 后续可验证实验

设计三个复杂度不同的任务（轻量清查、复杂 SDD、稿件验收），比较 Chat→GitHub→Codex/Work 路由与直接使用 Codex 的结果。只有在拥有任务质量、额度快照和工具记录后，才提出具体“节省比例”的结论。
