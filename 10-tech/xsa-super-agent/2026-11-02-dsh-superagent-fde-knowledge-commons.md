# 学习专题｜DSH Super Agent × FDE 知识公地（2026-11-02）

> 状态：进行中 · 事实来源：DeepSeek 官方 000–008 文档和行途现有公开仓库。当前未部署 DSH Super Agent、飞书机器人，也未创建 FDE 新仓。  
> 给读者可带走的东西：上游设计阅读路线、FDE 知识仓边界、跨仓知识索引方法及项目纠偏记录。

## 初始观察：原来我们人工做的接力，上游已经在做

ChatGPT Chat 规划→人工转述 Muse→Muse 通过浏览器/API 完成 GitHub 操作→GitHub 留下 PR/Commit→ChatGPT 审核。DSH Super Agent 的 GitHub/可选飞书 Source、Trigger→Eval→Ticket+Mandate→Assignment→Executor→Channel/Outbox 已覆盖**单仓主动代码代理**的主要交接结构。我们当前仍是人工接力，不应把 XSA Mock 误写为已有自动闭环。

**新的工程判断**：XSA 不重新做单仓 Coding Agent；优先验证 DSH 的 Source 扩展 Cookbook、Orca 的本地多 Agent 编排与 Orka 的 Gateway，寻找真正的跨产品适配缺口。

## 官方九份资料阅读路线

- [README](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/README.md)：研究原型、单 GitHub 仓、可选飞书、Web 面板与注意力原则。明确 **research prototype—not official production DeepSeek product**。
- [000 Philosophy](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/000-philosophy.md)：人类注意力成本、明确授权、正常静默、少概念。
- [001 Domain Model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/001-domain.md)：Source / Trigger / Thread / Eval / Ticket / Mandate / Assignment / Executor / Subscription；**上下文不等于授权**。
- [002 Authorization](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/002-authorization.md)：确定性 Gate、模型 Assessment、准入与授权版本。
- [003 Execution](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/003-execution.md)：每 Ticket 独立 Session/目录、失败恢复、重试与并发约束。
- [004 Prompts](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/004-prompts.md)：主 Session 路由与 Executor 决策分离；Prompt 不能越过 Host 权限。
- [005 Panel](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/005-panel.md)：只让需人工决策的事项占据注意力。
- [006 Deployment](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/006-deployment.md)：独立 DSH profile、GitHub bot 账号、可选飞书机器人与 `lark-cli`；先试验再接生产。
- [007 Architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md) 与 [008 Cookbook](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/008-cookbook.md)：Engine/Policy/Store/Outbox 分层与新增 Source 的流程。

## 用户纠偏：xingtu-fde 的真正定位

最初把 `xingtu-fde` 理解为“FDE 案例、Skills、售前工具和飞书入口”，这只覆盖其应用侧。用户进一步明确：它应当成为 **FDE 理论 + 行业研究 + 行途全部仓库知识关联 + 实战经验 + 商业假设的开放知识中枢**。

因此：
- XSA 是目标/专业 Agent 协作系统；FDE 是知识系统，二者可独立存在。
- 不把飞书机器人作为 FDE 的必选基础设施；它只是可能的查询/任务入口。
- 不把 `xingtu-skills`、`xingtu-sdd`、`xingtu-harness`、`xingtu-articles` 原文复制进 FDE；建立带来源、版本、许可证、验证等级的索引。
- 原文与发表版权分层：`xingtu-articles` 标记 CC BY-SA，引用与摘要保留来源，不直接改为 MIT 内容。
- FDE 商业机会是待测试假设，不能由 Super Agent 开源架构直接推断企业付费价值。

## 已存在的公开学习样本

| 主题 | 来源与证据边界 |
|---|---|
| FDE 工作法：进场、在场、离场 | [文章](https://github.com/xingtu1996/xingtu-articles/blob/main/articles/2026/09/2026-09-25-fde-working-method-three-stages.md)，行途已发表内容 |
| 资金报表流程改造 | [文章](https://github.com/xingtu1996/xingtu-articles/blob/main/articles/2026/10/2026-10-28-fde-fund-report.md)，正文明确标注第三方从业者自述，**不是行途亲历** |
| 海量评论数据清洗 | [文章](https://github.com/xingtu1996/xingtu-articles/blob/main/articles/2026/10/2026-10-28-fde-data-cleaning.md)，第三方案例转述 |
| AI 工程化四道质量门禁 | [文章](https://github.com/xingtu1996/xingtu-articles/blob/main/articles/2026/10/2026-10-26-four-quality-gates.md)，需核对正文数量主张，不应直接当独立审计证据 |
| FDE 能力模型 | [行途 AI Engineering](https://github.com/xingtu1996/xingtu-ai-engineering)，引用现有方法论与文章索引 |

## 可复用的研究方法

每条知识登记：`source_id / title / url / source_type / snapshot_sha / license / fact_or_hypothesis / confidence / privacy / last_verified`。案例卡再记 `business_problem / constraints / attempted_solution / measured_result / counterexample / reusable_pattern`。真实实践、第三方自述、合成示例不得混用。

## 开始实验前的待办

1. 由拥有建仓能力的 Muse 创建 `xingtu1996/xingtu-fde`，或核对是否已存在；建仓与初始文件都需返回链接及 Commit SHA。
2. FDE 仓先发布来源索引、知识地图和真实可用的学习卡，不为凑目录创建空文件。
3. 在隔离账号和实验仓内验证 DSH GitHub Source / Feishu Source，不动现有定时与客户环境。
4. 对知识检索、跨仓关联、工作成果回流各进行一个闭环实验；再决定是否需要自动同步、向量库或知识图谱。

**跨仓设计文件**：[XSA 的 FDE Blueprint](https://github.com/xingtu1996/xingtu-super-agent/blob/docs/dsh-superagent-fde-strategy-20261102/docs/research/FDE_PRODUCT_BLUEPRINT.md)。
