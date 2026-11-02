# XSA 学习记录 01｜授权摩擦与多 Agent 冲突（2026-11-02）

> 学习状态：进行中，首轮来自真实 UI 截图；已见到配置项，不代表完成了授权效果实验。  
> **读者可以拿走什么**：权限最小化检查清单、自动化验收表、XSA 控制平面设计问题。

## 触发问题

开发 `xingtu-super-agent` 时，用户在 ChatGPT 中定义目标，手动转述给 Muse。Muse 能通过浏览器创建 GitHub 仓库，并使用 GitHub 连接器推送文件；但每次写入都可能弹出「允许」请求。与此同时，ChatGPT 的 GitHub 工具也能在其他实验分支写入，于是产生“如果两个 Agent 同时动手，谁负责、如何阻止冲突”的问题。

## 已核实观察

1. Muse GitHub 设置中：读取仓库＝允许、更改仓库＝请求、后台同步＝允许。
2. Muse 全局设置中：连接器＝请求某些操作、网络＝请求某些操作。
3. Muse 浏览器建仓与 GitHub API/Connector 写入是**不同操作路径**，是否共用授权尚未验证。
4. XSA 研究分支和 Muse 初始化分支同时存在的风险已被用户指出，协调方改为只读/停止同目标写入。
5. 当前用户是“手工转发 ChatGPT 任务给 Muse”，并非 XSA 自动事件传递。

## 第一性原理提炼

真正的目标不是“让所有操作都不弹窗”，而是**减少重复的人工注意力开销，同时不降低权限边界**。权限控制应独立于 LLM 的自我判断，重试须有稳定操作 ID、状态和回执；Agent 并发必须有对象所有权和版本约束。

### 权限问题拆解

- 平台层：应用是否允许对某种动作持久授权？
- 连接层：GitHub App 能看到哪些仓库？是不是账户全局？
- 任务层：目标、分支、文件范围、有效期与最大操作次数是什么？
- 风险层：创建实验文件 vs 删除/公开/生产发布是否需要不同审批？
- 审计层：由谁批准、何时、完成了什么、远端有何证据？

**当前只见到设置标签，没有看到完整下拉选项。** “支持任务级批准”“始终允许所有写入”均不得在产品 README 写成已证实。

## 实验设计

| 实验 | A 基线 | B 方案 | 证据 |
|---|---|---|---|
| 授权摩擦 | 当前 Connector 写入＝请求 | 使用界面实际允许的最小范围授权 | 审批次数、任务范围、审计记录 |
| 执行通道 | 浏览器建仓 / Connector 写文件 | 单独标注 transport 和权限范围 | 真实仓库 URL、Branch、SHA |
| 双 Agent 冲突 | 两个 Agent 同时写文件 | Owner + Lease + CAS + 幂等键 | 重复副作用=0、冲突能暂停 |
| 成本效率 | 手工复制 Chat→Muse | XSA 事件 Task/Receipt | 人工交接次数、时间、质量 |

先只测试专用实验分支，不能把“允许”试验扩展到现有生产仓库，禁止绕过确认弹窗。

## XSA 的工程需求

- Capability Router：哪些 Agent 能处理什么动作，不要假设 ChatGPT/Muse/Codex 能直接调用对方的会话。
- Authorization Ledger：用户允许哪些 task/repo/branch/action、多久有效。
- Coordination Guard：Task Owner、租约、任务依赖、抢占和冲突降级。
- Evidence Receipt：输入版本、输出 SHA、审批依据、失败与恢复决策。
- Watchdog：只在越权、冲突、失败和明确需要人类决策时提醒；正常步骤静默。

## 项目与参考

- [XSA Case 002 原始证据整理](https://github.com/xingtu1996/xingtu-super-agent/blob/research/orca-orka-dsh-20261102/docs/research/2026-11-02-muse-github-permission-and-conflict-case.md)
- [XSA Orca/Orka/DSH 研究](https://github.com/xingtu1996/xingtu-super-agent/blob/research/orca-orka-dsh-20261102/docs/research/ORCA_ORKA_DSH_2026-11-02.md)
- [XSA 初始 Event Bridge PR](https://github.com/xingtu1996/xingtu-harness/pull/4)

## 下一次更新触发条件

取得 Muse 权限下拉框真实选项；执行低风险实验、形成截图与审计记录；或 Muse 初始化任务提交完成并产生可核实的 PR/Commit。每次更新将“已观察/已验证/推测/设计目标”单独标注。

---
**纠偏记录**：不以“关闭所有安全弹窗”为产品目标，而改为“受限授权下的低摩擦自动化”。这是一条从具体使用摩擦发展到控制平面设计原则的真实学习路径。
