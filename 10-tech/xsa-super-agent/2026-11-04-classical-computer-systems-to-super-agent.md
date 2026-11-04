# 从经典计算机系统到 Super-agent｜14 个长期可学的工程原理

> 2026-11-04｜学习笔记/研究索引，不是生产验证报告。面向行途的开发者和 FDE/Agent 工程实践。
> 作者区分：[原文] DeepSeek 官方设计；[经典原理] 计算机系统已有的独立方法；[类比] 对 XSA 的延伸；[实验] 尚待用 GitHub 任务验证。
> 原始线索：[官方 X 文章](https://x.com/DeepSeekHarness/status/2116857257245987236)、[DeepSeek 官方研究原型](https://github.com/deepseek-ai/dsh-superagent-prototype)、[原型哲学](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/000-philosophy.md)。

## 一、这套研究真正回答什么

**单任务能力受模型限制，多任务上限受人的注意力限制。** DeepSeek 作者将若干经典计算机系统机制应用到 Agent 协作——目标不只是更多 Worker，而是人只负责方向与最终验收。行途的 Chat / Work / GitHub 流程走在相同方向，但跨平台的自动会话同步、权限门禁、可靠重放等尚未部署；不能用仓库数量代替工程能力。

### 从原理到行途的四层概念图

- **Control Plane**：Router/策略/许可与 Watchdog，决定要做什么、能否做、何时需要人介入。
- **Execution Plane**：独立 Worker、可调用 Tool/Skill、异步执行与沙箱隔离。
- **State & Knowledge Plane**：Task/Receipt/事件日志、checkpoint、按需召回、GitHub 证据与领域知识。
- **Human Interface**：简短异常/批准请求与可审核的 PR/详细报告；注意力是稀缺资源。

以上是学习时的**抽象模型**，不是断言 DeepSeek 代码中存在四个同名类或 XSA 已实现完整四层。

## 二、14 项原理的学习卡与误区

| # | 关键词 | 先理解的经典概念 | Super-agent 对应 | 行途实践练习 |
|---|---|---|---|---|
| 1 | Compute / State / Environment 分离 | 无状态服务、持久数据、远端执行环境与故障域 | 原文 §5 三分离、端侧 daemon | 画出 XSA/GitHub/本地 Work 的运行和数据位置，指出机器离线可做与不可做的事 |
| 2 | Speculative Execution | CPU 预测分支结果先算后提交，区别于 MapReduce 掉队任务副本 | 原文 §3.4 早准备、有价值再交 | 只读复现一个 Issue，验证失败则只留内部报告，不发 PR；模拟审批门控 |
| 3 | Watchdog | 独立心跳、故障检测、恢复策略 | 原文 §6 独立 Watchdog Session | 对比进程 alive、任务 progress、目标 alignment 三种信号 |
| 4 | Feedback Control | 检测→误差→纠偏→复验；控制器、观察误差 | 原文直接称 Watchdog 外部控制回路；Router 是延伸类比 | 给进展停滞制定阈值和人工接管流程，分析误报与振荡 |
| 5 | Master/Worker | 控制与数据面职责分离、隔离故障域 | 原文 §2 Router 不执行，Worker 执行 | 演示 Chat/Work 的职责声明，比较仅 Prompt 委派和任务协议约束 |
| 6 | Event-driven / Trigger | 事件与轮询、消费者 offset、队列、去重、乱序 | 原文 §3 Trigger | 同一 PR 评论重复投递三次，检验是否只生成一个 Task |
| 7 | Fast Path / Slow Path | 确定性规则快筛 + 高成本语义判定 | 原文 §3.1 两层过滤 | GitHub 来源/白名单先审，再让模型判断是否有实际任务 |
| 8 | Batching | 合并高频输入摊薄固定成本、顺序与延迟 tradeoff | 原文 §2、§7.2 Router 批处理 | 同一 Task 的 10 个通知合并，一条撤销指令不能被吞掉 |
| 9 | Cache / Locality / Inline & Spill | 热数据、局部性、引用指针、缓存命中 | 原文 §3.3 Chain of Recall | 只给 Agent Issue ID + 摘要，按需读取 PR、Commit 和来源 |
| 10 | Backpressure | TCP 窗口、容量反馈、生产者节流 | **工程延伸**：人的通知容量与注意力节流 | 区分真正 queue backpressure 和“少通知”的产品策略 |
| 11 | Async / Nonblocking | Future、后台任务、事件回调与取消 | 原文 §4.1 start/stop；DSH 已实现但未默认启用 | 只在安全的模拟工具中验证 Started → finished/timeout/cancelled |
| 12 | Durable Execution / Checkpoint | event log、确定性 replay、Activity 幂等 | 状态外置是原文；Temporal/LangGraph/Saga 是额外技术路线 | 模拟崩溃后重放，不重复创建 Issue/PR；区分状态恢复和外部副作用 |
| 13 | Blackboard | 多专家共享结构化状态、事务和版本控制 | **松散类比**：原文是 Thread 多 Worker 订阅 | 两个 Worker 同时读写同一 PR，记录 SHA 冲突与 owner 策略 |
| 14 | Human Cognition / Chunking | Miller 7±2 与 Cowan 约四组块研究 | 原文说作者经验“3–5 个活跃 Session”，不是正式认知实验 | 用 GitHub 项目索引减少人工记忆负担，统计每周上下文重述次数 |

### 重点分辨：概念相似不代表“该系统已经实现”

**投机执行**：MapReduce 是复制延迟任务竞速；CPU 是不确定结果时提前计算；DeepSeek 的“静默复现并修复”更像第二种“先准备、后决定是否交付”，但真实外部副作用不能像 CPU 指令一样凭回滚缓冲撤销。

**Backpressure**：让下游容量信号约束上游输入，是明确的协议；“IM 只告诉用户必要的事”是注意力层面的流量整形。它们可借鉴，不应写成同一机制。

**Blackboard**：共享事件订阅并不保证共享强一致状态；同一个 GitHub Thread 被多个 Worker 看见，不能替代文件租约、版本校验。

**人的 3–5 个活跃会话**：是 DeepSeek 团队的实践观察；Cowan（2001）的短期记忆约四个组块是另一种实验范畴，不能直接相减或当成“每人最多四个 Agent”的严格定律。[Cowan 论文](https://pubmed.ncbi.nlm.nih.gov/11515286/)。

## 三、拿一个真实生活化案例串起来

某个 GitHub 项目的 CI 报错。

1. GitHub Source 收到事件。第一层过滤只接收已授权项目、去重的可信事件。
2. Router 根据原有 Task/Issue/PR 关联同一个 Thread，不为每次 CI 失败都新开 Agent。
3. Worker 在隔离环境尝试复现，只允许读或写自己的测试分支。
4. Worker 如果明确复现故障，则在 Draft PR 留补丁与测试证据；否则写 failed/not_reproduced，不制造“成功”。
5. Watchdog 独立检查进展是否真实、失败是否持续、是否需要人类决定。
6. 需要发布/合并时，人类审批；审批后可验证回执返回 GitHub。
7. Learn/FDE 只沉淀事实、方法和来源，其他仓引用它们，不复制整段聊天。

这个流程目前是**设计实验计划**，不是 XSA 已在生产自动运行。

## 四、性能数字：只作为研究信息

DeepSeek 原文 §7 的 **合成调度实验**：每次约 300 条消息（其中约 20 个工作请求），编程步骤是消耗时间的模拟工具，各配置运行五次。

| 方案 | p50/p95 完成时间（分钟） | 每轮读缓存 Token |
|---|---|---|
| Super-agent | 12.4 / 15.7 | 约 2320 万 |
| Super-agent 去掉 Pass-through | 12.6 / 15.5 | 约 3180 万 |
| 单 Session + Subagent（中性提示） | 20.4 / 29.5 | 约 610 万 |
| 单 Session + Subagent（偏好委派） | 13.8 / 29.0 | 约 1080 万 |

Router 约每分钟 1→40 条触发、平均 batch 1.0→2.8、摊到决策上的推理 6.4→1.6 秒。表明在该负载下批量处理有利于调度吞吐，但**不是**真实代码质量、ROI 或 Plus 额度节省测量。Super-agent 读缓存 Token 高于单会话基线，亦需考虑人力和 Token 两个成本。

## 五、进阶工具与理论阅读顺序

**阶段 1（2–3 次学习）**：计算/状态分离、Router/Worker、Trigger、Fast/Slow，读 DeepSeek 官方文章 §2/§3/§5；产出一张“当前 XSA 并未实现什么”的架构差距表。

**阶段 2（2–3 次学习）**：幂等、checkpoint、异步、Watchdog、事件回放；读 [Temporal Workflows](https://docs.temporal.io/workflows) 的 Event History/replay，以及 [LangGraph Persistence](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx) 的 Checkpointer/Store 区别。不要把 Temporal 当“快照直接恢复”：它通过记录的事件历史确定性 replay，外部 side effect 要分离到 Activity 并考虑重试语义。

**阶段 3（1–2 次学习）**：订阅、缓存召回、Blackboard 与人的注意力，研究 DeepSeek §3/§4/§6，并提出 1 个真实行途任务的交接卡和审批设计。

**阶段 4（实验）**：选择 FDE PR 的重叠文件或 XSA Event Bridge Mock，执行三个离线 T 用例：重复事件只认领一次、权限不足阻止副作用、失败重放不会重复创建 PR。保存代码版本、真实运行结果与未覆盖边界。

## 六、15 分钟自测（不是死记术语）

1. 一个 Worker 还活着但两小时没有交付，alive 和 progress 哪个信号出错？如何判别？
2. 已给用户发了一封邮件再说“投机失败丢弃”为什么不成立？
3. 只靠 GitHub Issue 对同一文件写入，为什么不能宣称已锁定？
4. 为什么降低用户的打断次数可能提高 Token 消耗？
5. 应该先在 XSA 加数据库还是先给 Task 加稳定 task_id 与 input_sha？如何验证？
6. Temporal Event History 和 LangGraph Checkpoint 有何实现差异，分别有什么代价？

## 七、跨仓学习与工程链接

- XSA 研究稿：[14 项原理及证据分层](https://github.com/xingtu1996/xingtu-super-agent/blob/research/deepseek-classical-systems-cascade-20261104/docs/research/2026-11-04-superagent-computer-systems-principles.md)
- XSA 级联矩阵：[开源矩阵的职责与协议传播](https://github.com/xingtu1996/xingtu-super-agent/blob/research/deepseek-classical-systems-cascade-20261104/docs/architecture/2026-11-04-open-source-matrix-cascade.md)
- 官方研究原型的 [README](https://github.com/deepseek-ai/dsh-superagent-prototype) 与 [授权](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/002-authorization.md)
- 额外参考：[LangGraph Persistence](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx) / [Temporal Workflows](https://docs.temporal.io/workflows) / [Cowan 2001](https://pubmed.ncbi.nlm.nih.gov/11515286/)

## 学习成果的验收标准

能够独立讲清楚 14 项思想中哪些是原文直接机制、哪些是经典学术理论、哪些只是行途延伸；画出完整权限和副作用边界；完成至少一次有 commit/test/PR 可追踪的 Mock 实验。**没有动手测试，仍然只是学习记录。**
