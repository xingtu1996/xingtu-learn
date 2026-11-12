# 学习实验 03｜会话命名驱动：Chat → Work → GitHub

> 2026-11-02 · 工程过程记录，非验收报告。照片证据存于用户 Library 的 `/XSA_工程实践素材`，公开文档仅提供素材清单，后续发布时再审核截图。

## 触发点：为什么每次新开会话都像重启项目？

在行途已有 FDE、AI 工程化、Skills、Harness、XSA 等项目，长期会话同时存在 Chat、Work 与 Muse/Codex。过去的问题不是 AI 完全不会做，而是目标、能力、权限、执行状态和成果散落在聊天里，换一个会话就得人工重复交代。

于是用户为专业会话采用固定格式：

- `XSA (chat)｜Super Agent 工程总控`
- `XF (chat)｜FDE 知识与工程实践`
- `XSA (work)｜Super Agent 工程实施`
- `XF (work)｜FDE 工程建设`（目标命名）

尝试第一次流程：先在 Chat 形成 XF 工作任务包，在新 Work 会话选择 **GPT-6.1 Sol / 高**，输入主仓、总控仓、边界、交付方式与模型分工，然后由 Work 实施，准备通过 GitHub PR 留证。

## 本次截图可以证明什么

1. Work 的输入包含项目、主仓、总控仓、职责、模型推荐、推理强度和 Draft PR 交付约束。
2. 运行界面显示已选择 GPT-6.1 Sol、推理强度为「高」。
3. 左侧正在使用的会话名称却是 `XSA (work)｜Super Agent 工程实施`，与消息的 `XF (work)｜FDE 工程建设` **不一致**。
4. 截图处在执行和重新连接状态，不包含最终 PR 交付或测试结果。**不能说已经成功自动完成 FDE 建仓**。
5. 本次仍通过手动建立 Work 会话来触发，并非 XSA 自动监听普通 Chat 的消息。

## 从错误里得到什么

**会话名称只能帮助人类找到工作，不能充当机器分派任务的唯一凭据。**

用户想要的是：Chat 规划/裁决、Work 工程实施、GitHub 事实/交付。但 Work 接受的实际项目身份应由 `project + primary_repo + task_id + branch` 确定，不能根据名称中的 XSA/XF 直接猜测。

相比只用一段提示词，下一步更有价值的是在仓库中维护轻量 Session Binding/任务契约，把 Project、Role、Status、Policy、模型和证据字段固定下来。

## 规范 v1

| 项目 | Chat 的任务 | Work 的任务 | GitHub 的任务 |
|---|---|---|---|
| XSA | 架构/治理/研发取舍 | 代码、联调、测试、PR | 设计记录、可复查的工作凭证 |
| XF | 理论知识、FDE 业务分析 | 索引/知识卡/工具/工程交付 | 来源台账与公开知识资产 |
| Learn | 学习计划与理论比较 | 可复现实验、批量资产治理 | 实验、纠偏和回溯 |

**默认规则**：每个专业会话绑定一个主仓，可引用多个其他仓；一仓可有多个专业会话，但不允许没有分支所有权的并发写入。

## 可执行的验收路径

- 核对正在运行的 Work 是否真正产生 PR、Commit SHA 与测试证据。
- 修正 `XSA (work)` 对应 XF 实施任务的会话标题，并在 Work 内声明真实 `primary_repo`。
- 下次启动前从绑定文件读取，再发起任务，记录是否减少人工补上下文次数。
- 对比出错前后的任务归属正确率、跨会话交接次数、批准次数和合格交付耗时。

## 分享价值

这是一种低技术成本的 AI 工程工作法，不需要先做平台：**取明确的会话名 → 任务用 GitHub 跟踪 → 用专业 Agent 实现 → 必须给出可核验回执。**

但标题并不等于真正的自动绑定；任何模型选择也应区分“提示词中建议”与“Work UI 实际选择”。以上知识都源于实际截图，不是产品已实现声明。

### 关联

- [XSA 主仓 Case 003](https://github.com/xingtu1996/xingtu-super-agent/blob/docs/case003-chat-work-repo-bound-20261102/docs/history/cases/CASE-003-chat-work-repo-bound-conversation.md)
- [XSA Case 002 授权和并发治理](https://github.com/xingtu1996/xingtu-super-agent/pull/1)
- [XSA 原型与 DSH 深读](https://github.com/xingtu1996/xingtu-super-agent/pull/2)

## 截图素材存放说明（仅用户可访问）

- Library：`/XSA_工程实践素材/CASE003_2026-11-02_original_private.png`
- Library：`/XSA_工程实践素材/CASE003_Work任务与模型_局部截图.jpg`
- Library：`/XSA_工程实践素材/CASE003_会话命名_局部截图.jpg`

原图有其他聊天列表信息，禁止在公共仓未经审查上传。局部裁剪图也需要发布前检查 UI 标识与具体敏感项。
