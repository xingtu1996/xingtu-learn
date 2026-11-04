# W-03｜Chat 转 Worker 工作空间漂移：一次完整的 Agent 事故现场还原

> 类型：工程实践踩坑（教材版）| 标签：Worker、Codex、工作空间、Harness、上下文装载、Agent 事故
> 事故日期：2026-11-03 | 教材版本：v1.0 | 定位：可直接做知识付费案例

---

## 一、事故现场

### 发生了什么

公众号《主题修订审阅》一篇文章，在 Chat（豆包办公）里讨论完，转成 Worker（Codex CLI）去执行排版和发布。
结果 Worker 在错误目录下生成了 v1→v2→v3→v4→v5 五个版本，返工到第五版才被发现：

- 视觉不对：HTML 里 `#F2644F` 只有 12~13 处，未达 DESIGN.md §三"通栏级 20+ 处"
- 目录混乱：`02_封面/` 和 `03_封面/` 并存、`04_配图/` 和 `04_公众号排版/` 并存
- 逻辑不顺：正文是 boss 当晚手工纠偏后才顺的，不是 AI 直出就对

### 根因一句话

Worker 启动时 cwd 是 `~/Documents/Codex/2026-11-03/`（默认工作区），
**没有切到 `<行途工作空间根>`**，
导致零行途上下文——没读 AGENTS.md、没读 DESIGN.md、不知道 publish-pack-planning 五闸门。

---

## 二、为什么 Chat 里好好的，转 Worker 就崩了

这是最有商业价值的洞察。

| 维度 | Chat（豆包办公） | Worker（Codex CLI） |
|---|---|---|
| 项目规则装载 | 项目 AGENTS.md 全文 + 70+ skill 元数据 + 用户偏好，直接注入系统提示 | 只自动读 `~/.codex/AGENTS.md`（34 行通用规范） |
| skill 发现 | 启动时已列出全部 skill 描述和触发词 | 需主动读 `.agents/skills/<name>/SKILL.md`，不读就不知道存在 |
| DESIGN.md 可见性 | AGENTS.md 铁律第 12 条直接引用阈值 | 全局 AGENTS.md 零行途上下文；项目 AGENTS.md 虽有引用，但读不读、读多深取决于模型自己 |
| 记忆持久性 | 跨会话保留用户偏好、项目规则 | 每次启动重新读文件，靠文件系统留痕 |

**结论：Chat 稳定不是因为它有独立记忆体，是因为它把行途完整规则集作为系统提示强制注入了。**
Worker 不是记忆差，是它启动时拿到的上下文本来就薄——除非项目 AGENTS.md 写得足够硬、足够短、足够指向关键文件。

---

## 三、六个根因（按证据强度排序）

| 编号 | 根因 | 证据 | 置信度 |
|---|---|---|---|
| E | 验收只查文件存在，不查视觉和逻辑 | pkg-healthcheck 逐包 `test -f`；Step 9b 11 项核查无一项查叙事结构 | 高 |
| A | "基础视觉叙事规范"是孤立 Draft，没进运行时上下文 | `work/design-v4/01_视觉叙事规范.md` 文件头标 Draft；无任何 skill/AGENTS.md 引用 | 高 |
| B | 多份规范冲突，活 skill 还在用被禁的旧色 | concept-anchor-figure 原用 #d71a1b/#056DE8；10-visual-designer 原用行途蓝主色 | 高 |
| D | 编排层漏调下游视觉技能，无叙事骨架闸门 | publish-pack-planning 五步无"叙事类型选择"；mp-publish-sop Step 1b 不查骨架 | 中高 |
| C | 全局 Codex 入口零行途上下文 | `~/.codex/AGENTS.md` 34 行只有通用规范 | 中 |
| F | 模型/额度/宿主限制 | config.toml 显示 gpt-6-luna / priority / 1M context；不是额度问题 | 未知 |

---

## 四、三层防护（已落地）

### L1 默认工作区指路牌

`~/Documents/Codex/AGENTS.md` 写"你走错了，去 <行途工作空间根>"。
Worker 启动读 cwd AGENTS.md 时被拦住。

### L2 Chat→Worker 入职提示词

见同目录 `W-03-worker-onboard-prompt.md`。
Chat 转 Worker 时贴给 Worker，强制 cd + 读 AGENTS.md + 读 DESIGN.md。

### L3 全局硬规则

`~/.codex/AGENTS.md` 末尾从"指针"升级成"硬规则"：
Worker 启动三步：`pwd` → `cd` → 读项目文件。

### 第四层（规则工程化）

`xingtu-rules/specs/XRULE-002/workspace-anchoring.md`：
P0 优先级，三层防护表 + 信息源路径表 + 换设备同步清单。

---

## 五、治理清单（2026-11-03 当晚完成）

| 文件 | 修复 |
|---|---|
| concept-anchor-figure/SKILL.md + metadata | #d71a1b/#056DE8 → #F2644F/#1a1a1a |
| skill-routing.md | concept-anchor-figure 路由描述去行途蓝 |
| 10-visual-designer.md | 行途蓝主色 → 三原色白底 |
| publish-pack-planning/SKILL.md | 黑白交替 → 统一白底；加 Step 0.5 叙事骨架闸门 |
| mp-publish-sop/04.md | F2644F 门禁 >0 → ≥20（通栏级） |
| DESIGN.md §八·补 | 加叙事骨架指针 |
| ~/.codex/AGENTS.md | 加行途工作区锚定硬规则 |
| ~/Documents/Codex/AGENTS.md | 放默认工作区指路牌 |

备份：`.backups/20261103-233506-visual-narrative-fix/`

---

## 六、PR 落档（6 仓同步）

| 仓 | commit | 内容 |
|---|---|---|
| xingtu-harness | d290f83 | content-production-harness 合并 |
| xingtu-super-agent | 59e755f | workbuddy-adapter 合并 |
| xingtu-vault | f9d6ae39 | 80 个散件归档 + content/doubao-distill 合并 |
| xingtu-design | 15dc4de | 视觉叙事实验 4 组 HTML/PNG |
| xingtu-sdd | a3b52c5 | 治理 spec |
| xingtu-rules | 3a67f0c | XRULE-002 工作空间锚定 |
| xingtu-learn | 121e764 | 本文 + 入职提示词 |

---

## 七、可复用方法论（知识付费素材）

### 1. Agent 事故第一查：工作空间

产出不对时，先查 `pwd`，不是先查模型、不是先查 prompt。
cwd 不对 = 零项目上下文 = 瞎干。

### 2. Chat 和 Worker 是两种宿主

- Chat = 系统提示注入式（启动即知一切）
- Worker = 文件读取式（我不读文件，我就不知道）

设计 Agent 工作流时，必须假设 Worker 拿到的上下文比 Chat 薄 80%。

### 3. 门禁不能只查文件存在

`test -f` 只能确认文件在，不能确认文件对。
视觉规范要查色值数、叙事结构要查骨架类型、逻辑要查层层递进。

### 4. 三层防呆结构

- 底层：默认目录放指路牌（最低成本）
- 中层：入职提示词模板（可复用）
- 顶层：全局硬规则（工程化）

### 5. 换设备/路径变更清单

规则硬编码了绝对路径时，必须同步更新三处：
1. 项目根 AGENTS.md
2. 全局 ~/.codex/AGENTS.md
3. learn 踩坑记录（本文）

---

## 八、商业化角度（知识付费能讲什么）

- **"为什么你的 AI 在瞎干"**——Agent 工作空间漂移是通用问题，不是行途独有
- **Chat 和 Worker 的本质区别**——系统提示注入 vs 文件读取，这是很多人不知道的
- **SOP 有门禁为什么还会漏**——阈值软化 + 验收只查文件 + 宿主差异三重叠加
- **三层防呆工程**——从指路牌到硬规则，成本递增但确定性递增
- **真实事故复盘**——v1 到 v5 返工、色值数不够、目录混乱，全是可截图的真实证据

---

## 九、证据限制与遗留

- 11-03 当晚 v3→v4→v5 返工的真实执行宿主/模型未取证
- design-v4/01 仍是 Draft，boss 尚未正式拍板升格为 SSoT
- design / fde / rules 三仓本地特性分支未删，等 GitHub 侧 PR 确认关闭
- reasoning_effort 建议从 medium 提到 high，尚未改配置

---

## 关联文件

- 入职提示词：`W-03-worker-onboard-prompt.md`（同目录）
- 治理执行文档：`xingtu-sdd/specs/202611040000-visual-narrative-governance/spec.md`
- 规则工程化：`xingtu-rules/specs/XRULE-002/workspace-anchoring.md`
- 视觉实验对照：`xingtu-design/proposals/2026-11-03-visual-narrative-experiments/`
- 散件归档：`xingtu-vault/15_内部沉淀与临时/outputs根散件归档_2026-11-04/`
