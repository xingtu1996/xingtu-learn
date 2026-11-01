# W-02｜行途 AI Harness / Codex 智能路由实验任务包

- 日期：2026-10-31
- 状态：待实施；本文件仅为方案与交接，不代表本地 Codex 已配置
- 目标仓库：xingtu-learn；实施目标：后续由 Codex 在实际项目中验证
- 公开信息仅使用“行途 XingTu”，不记录姓名、账号密钥、邮箱、本地绝对私人路径

## 目标与边界

当前 Plus 账户在 Codex 桌面端使用 Astra 容易触及五小时窗口。目标是让 Sol 默认负责规划/常规 SDD，按需委派 Luna 做检索、Terra 做实现，只有高风险架构或困难问题才升级 Astra。优先使用原生 Codex Subagents，不急于开发 SDK 路由平台或购买 Business Standard。多 Agent 会独立消耗额度，是否节省必须实测。

Chat → GitHub → Codex 桌面端本地项目 → PR → 人审合并/发布。正式发布绝不自动执行。

## 官方依据（2026-10-31 核对）

- 本地 Codex 可通过 `.codex/agents/*.toml` 分别设置 Agent 模型和推理强度；桌面版可显示子 Agent 线程。https://learn.chatgpt.com/docs/agent-configuration/subagents
- 个人默认配置为 `~/.codex/config.toml`，可信项目可用 `.codex/config.toml` 覆盖；更高优先级配置可能覆盖默认值。https://learn.chatgpt.com/docs/config-file/config-basic
- 2026-10-29 Pro 100/500 的 Work/Codex 包含额度翻倍；Plus 未列入该次公告。https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes

## 角色建议（以账户实际可用型号为准）

| Agent | 推荐模型 | 努力程度 | 职责 |
|---|---|---|---|
| 主会话 | gpt-6.1-sol | medium | 任务澄清、Plan、SDD、调度、验收 |
| researcher | gpt-6-luna | medium | 只读检索、素材分类、摘要 |
| executor | gpt-6.1-terra | medium | 明确任务的实施、测试、文档生产 |
| architect（按需） | gpt-6-astra | low 起步 | 疑难问题、架构取舍、关键审核 |

启动原则：简单任务由主会话直接完成；独立工作才分派；默认最多两个并行 Agent；同一文件写入须协调；只在说明理由后升级 Astra。

## 项目级配置候选（先审计，后实施；不可覆盖原文件）

```toml
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"

[agents]
enabled = true
max_concurrent_threads_per_session = 2
default_subagent_model = "gpt-6-luna"
default_subagent_reasoning_effort = "medium"
```

`.codex/agents/researcher.toml`：

```toml
name = "researcher"
description = "仅负责边界清晰的只读检索和整理"
model = "gpt-6-luna"
model_reasoning_effort = "medium"
developer_instructions = "只读工作；返回来源与结论，不修改文件。"
```

`.codex/agents/executor.toml`：

```toml
name = "executor"
description = "根据批准的计划执行可逆修改并验证"
model = "gpt-6.1-terra"
model_reasoning_effort = "medium"
developer_instructions = "只执行明确任务包；运行测试；禁止擅自合并或正式发布。"
```

`.codex/agents/architect.toml`（可选）：

```toml
name = "architect"
description = "复杂决策、架构争议与重大风险审查"
model = "gpt-6-astra"
model_reasoning_effort = "low"
developer_instructions = "仅在主 Agent 明确升级时分析高难问题；提交风险、替代方案与验收条件。"
```

## AGENTS.md 待增补规则（先比较已有规范）

1. Sol 默认主协调；不让 Astra 负责日常检索和执行。
2. 简单只读工作可委派 researcher；规格明确的实施委派 executor。
3. 仅对复杂架构、关键风险或反复失败调用 architect；记录升级理由。
4. 不为并行而并行；子 Agent 的额外用量纳入总体统计。
5. 生产发布、外部消息、不可逆操作、PR 合并均保留人工门禁。
6. 所有结果必须提交实际证据、测试情况、文件差异和失败原因。

## Codex 后续启动任务（可直接复制）

“请以本任务包为执行依据，先只读盘点当前项目的 config.toml、AGENTS.md、.codex/agents、实际 model_provider 和 cc switch 影响，检查 Codex 桌面端/CLI 使用的配置与模型目录。仅报告脱敏结果，不读取或展示令牌。先出 SDD 和变更清单，不要修改任何历史配置。经确认后在独立分支/PR 中以最小差异创建 researcher、executor；architect 作为可选 Agent。运行下面三个测试，提供质量/用量对照；不得发布或合并。”

## 三类验收与记录

1. **只读盘点**：研究 Agent 从 xingtu-vault 找到真实内容流水线入口与文件证据；不能修改。
2. **SDD→可逆实现**：新建一份测试性文档或演示发布包，executor 按验收标准执行并测试；不得覆盖历史文件。
3. **疑难升级**：复杂质量门禁案例先由 Sol 判断，确有必要再调用 Astra；记录升级理由与结论。

每个用例记录：任务 ID、模型、effort、主/子 Agent、开始结束时间、是否升级、可用的五小时/周额度前后、结果质量、测试证据、失败原因。不要假定消息数等于实际额度。

通过条件：三类测试可复现；无越权发布或写入；质量不低于单 Agent 基线；实测总额度更优或能明确说明未优化的原因。失败时回退单 Agent。

## 交接与实施边界

本文件作为普通 Chat 到 Codex 的版本化交接真源。桌面版在本地项目中可以附加此前的 ChatGPT 会话（界面支持时），但执行必须以本文件及仓库最新状态为准。**当前只创建任务包，不修改任何现有配置，不运行测试，不部署。**
