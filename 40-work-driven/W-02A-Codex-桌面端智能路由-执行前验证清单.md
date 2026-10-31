# W-02A｜Codex 桌面版智能路由：执行前验证清单

> 状态：**待本地验证**｜2026-11-01｜从 W-02 衍生的独立补充文档，不修改历史文件或本地配置。
>
> 上游任务包：[W-02 智能路由实验](./W-02-Codex-Harness-智能路由实验-任务包.md)
>
> 本文档只包含可复核的执行方法与验收门槛。公开仓库中仅使用“行途 XingTu”，不得提交本地用户名、私人路径、邮箱、Token、代理密钥、会话日志原文。

## 一、先明确什么能实现

目标是**Codex PC 桌面版 + ChatGPT Plus 登录 + 项目级策略**完成模型分工：主 Agent 处理任务规划和验收，必要时委派专用子 Agent。**不要求改用 CLI**；CLI 用于诊断和复现时才加入对照。系统可能遵循路由提示词选择 Agent，但这不是可保证的、逐任务确定性模型路由，更不等于无限使用 Astra。

> 核心区别：`model` 是模型默认值；`AGENTS.md` 是任务行为规则；自定义子 Agent 是独立执行配置。任何一项都不能单独保证四模型自动切换。
>
> 独立的 **Agents API / Responses API** 有自己的 API 计费与多 Agent 配置，不应与 ChatGPT Plus 下的 Codex 桌面客户端配置键混用。

## 二、必须先核对的事实（不要根据草案直接修改）

| 项目 | 验证方法 | 放行条件 |
|---|---|---|
| 桌面版确实以 Plus 登录 | Codex App 账户/会话页面 | 记录账户类型，不截图或提交个人信息 |
| 配置层与实际 provider | 只读核对用户级与项目级 `config.toml`，检查 UI 当前选择及运行时输出 | 能判断使用官方 provider 还是本地代理；不读取任何密钥值 |
| 项目受信任及读取规则 | 检查 Codex App 对项目的信任状态及项目配置是否加载 | 新会话能读取目标项目配置 |
| Subagent 配置字段 | 查当前安装版本对应的 **Codex 本地客户端官方配置参考** | 每一个键均在该版本文档/帮助中得到确认 |
| 模型 ID 与访问权 | 用 App 中可选模型及当前客户端支持的模型列表核对 | 不假设 `gpt-6.1-sol`、`gpt-6.1-terra`、`gpt-6-luna`、`gpt-6-astra` 字符串一定是可配置的模型 ID |
| 子 Agent 可用范围 | 新建临时测试会话并检查角色是否可调用、模型是否独立生效 | 有可审计的会话输出及角色/模型信息 |
| `cc switch` 影响 | 只读比对代理配置启用与否，以及 provider 的最终值 | 结论基于当前状态，而不是“安装了代理所以一定走代理” |

**特别注意：**W-02 里 `[agents] enabled`、`max_concurrent_threads_per_session`、`default_subagent_model` 等字段及 `.codex/agents/*.toml` 的具体 schema 尚未在本次工作中逐项验证。**此时它们是候选草案，不得原样覆盖生产配置。**Agent 类型、并行上限字段与具体模型字符串，必须按当前 Codex 客户端官方配置说明验证后才能部署。不要把 Agents API 的 `agent.multi_agent.enabled` 或 `max_concurrent_subagents` 当成桌面客户端 TOML 键。

## 三、最小交付步骤

1. **只读盘点**：检查目前的 `AGENTS.md`、用户级/项目级 config、`model_provider`、App 当前选择、Codex 版本及可用模型。绝不输出凭据。
2. **产出 SDD**：记录当前状态、目标行为、正式支持的 TOML 键、配置优先级、迁移差异与风险；先给出变更 diff。
3. **隔离实验**：在临时分支、临时目录或新的 Codex 会话中验证；首轮只启用“主 Agent + 一个只读 researcher”，避免四模型全部并发。
4. **评估后扩展**：加入 executor，最后按需增加 architect；只在事实证明需要时调用高成本模型。
5. **交付 PR**：只提交新增的文档/经过验证的项目级配置；**不得**改写 `~/.codex/config.toml`，也不得更改实际发布流程。
6. **人工审核**：确认质量和额度数据后再决定是否采纳，遇失败可完全撤销项目级新增文件。

## 四、三个测试的验收数据

| Case | 任务 | 基线 | 路由实验 | 通过标准 |
|---|---|---|---|---|
| T1 | `xingtu-vault` 只读内容生产流水线盘点 | 单 Agent | 主 Agent + researcher | 关键文件、入口、证据一致；0 文件修改 |
| T2 | 演示性发布包（非真实发布） | 单 Agent | 主 Agent + executor | 新文件可复现、检查通过；不触及历史稿件 |
| T3 | 高风险质量门禁方案评审 | 单 Agent | 主 Agent 判断→必要时 architect | 记录升级理由；风险覆盖率不降低 |

逐次记录：任务 ID、工作树状态、会话时间、实际模型、推理强度、子 Agent 数、升级触发、完成率、复工次数、测试证据、可获得的 5 小时/周额度前后值。**使用率百分比和 Token 数可能不等价**；无法读取就记“缺失”，不得编造。

推荐结果表：

| task_id | arm | model/effort | subagents | elapsed | 5h_before/after | quality | outcome |
|---|---|---|---|---|---|---|---|
| T1 | baseline | 待测 | 0 | 待测 | 待测 | 待测 | 未执行 |
| T1 | routing | 待测 | 待测 | 待测 | 待测 | 待测 | 未执行 |

每个 Case 先后对照相同输入（或等价工作量），重复至少两次，控制文本长度/外部工具差异。结论分开统计 **用量、时长、质量**：减少时长不代表减少额度。

## 五、分工策略（行为规范草案，非运行保证）

- **默认主 Agent：Sol（若 App 实际支持）**：梳理需求、常规 SDD、协调与结果验收。
- **researcher：Luna（若支持）**：简单检索/分类/引用核对，优先只读。
- **executor：Terra（若支持）**：接受清晰任务包后执行、测试与交付。
- **architect：Astra（若支持）**：架构冲突、反复失败或重大风险才升级。
- 先单 Agent，确有独立的工作再启动子 Agent；默认实验上限 **两个**，须由当前客户端支持的正式字段设置。
- 所有外部发布、仓库合并、破坏性操作均需人工确认。

## 六、Codex 桌面版交接提示词

```text
请打开本地项目并阅读 xingtu-learn/40-work-driven 下的 W-02 与 W-02A 文档。
本轮严格只读。先核对 Codex 桌面 App/CLI 版本、Plus 登录状态、
配置优先级、实际 model_provider、自定义代理对 App 的影响、
项目现有 AGENTS.md 和可用模型及 Subagent 支持。
不要读取、打印或提交任何密钥、完整会话日志和个人路径。
请交付一份《现状审计 + 官方可用配置字段对照 + SDD + 最小 diff + 回退方案》。
对于 W-02 草案中未经确认的 TOML 键和模型 ID，请明确标注“未经验证”，
不要写入实际配置，更不要直接替换 ~/.codex/config.toml。
等待我审核 SDD 后，再执行隔离实验。不得发布文章、合并 PR 或覆盖历史稿件。
```

## 七、完成定义与下一轮决策

- [ ] 本地实际 provider 与模型列表已验证
- [ ] 每个配置字段有当前客户端依据
- [ ] 至少跑通一条主 Agent→子 Agent 委派
- [ ] 三个 Case 有可复现的单 Agent 对照数据
- [ ] 无历史文件修改、无意外发布、无秘密信息泄漏
- [ ] 成本/质量有数据支持；无收益则回退单 Agent

**本次 GitHub 文档工作不是本地实验。**不要将“文档已经提交”表述为“自动路由已经部署”。

参考：Codex 配置层 https://developers.openai.com/zh-Hans/docs/config-file/config-basic ；Agents API 与 Codex 客户端是不同的配置界面 https://developers.openai.com/api/docs/guides/agents-api/multi-agent 。
