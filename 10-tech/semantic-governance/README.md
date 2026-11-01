> status: 活跃 ｜ 建立: 2026-10-30 ｜ 阶段: 文献与源码审阅已完成；样例执行/资源评测待验证
> 读者能拿走什么：一张数据治理分层对照表、一组全合成的 FDE 交付门禁数据、一段标准库基线、一段 Semantica 图谱实验、一张部署成本/价值验收清单。

# 从数据治理到 AI 可执行知识：Semantica / Context Graph 实践

> 研究对象：[semantica-agi/semantica](https://github.com/semantica-agi/semantica)（MIT）。本目录是独立技术学习，不代表项目合作、客户案例或已上线方案。

## 为什么学习

**核心问题不是能不能做一张知识图，而是何时值得把文档和日志升级为机器可查询的语义关系、显式约束与决策证据。**

- **对个人工作空间**：Markdown / Git / Obsidian 足以承担原始记录、版本管理、可读笔记。Semantica 可作为*可选的派生语义索引*，不应取代源文件。
- **对 Agent / FDE**：当需求变更、审批、测试、发布决策跨多个记录、需要形式化核验与追溯时，可选地引入关系、溯源与规则层。
- **对企业**：定位于语义/知识治理与决策可追溯，不等价于完整的数据资产治理平台。

## 分层对照：梳理、治理、语义、决策

| 层次 | 核心问题 | 代表产物 | Semantica 角色 |
|---|---|---|---|
| 数据梳理 / 盘点 | 有哪些数据、在哪 | 数据源清单、表结构、业务流程 | 可接入/抽取，不负责组织资产盘点全部流程 |
| 数据治理 | 数据标准、质量、责任、权限、生命周期如何落实 | 质量规则、目录、责任人、权限流程、主数据 | 可提供关联/校验组件，不能替代制度与权限执行 |
| 语义治理 | “客户”“需求”“审批”在不同系统中的确切含义 | Ontology、受控词表、实体映射、语义约束 | **核心适配** |
| 决策治理 | 谁在什么证据和规则下做了什么决策 | Provenance、决策记录、审计链、阻断理由 | **核心适配** |
| 应用/Agent | 谁消费、如何执行 | MCP、API、GraphRAG、工作流 | 作为可选上下文服务 |

**注意**：有源 ID ≠ 源可信；有 PROV-O 数据 ≠ 自动符合法规；规则引擎 ≠ 自动识别伪造审批；GraphRAG ≠ 自动消除幻觉。原始事实认证、权限隔离、政策制定和审计独立性仍由业务系统承担。

## 与相关路线的比较

| 方案 | 强项 | 典型限制/取舍 |
|---|---|---|
| Obsidian + Markdown | 人类阅读、连接式笔记、低成本可迁移、Git 可版本化 | 复杂跨系统语义约束与执行规则需额外实现 |
| SQL + Python / 结构化日志 | 少量明确规则、低成本与易审计 | 大量多跳异构关系后查询与模型维护压力增加 |
| 普通 RAG / 向量库 | 非结构化资料的语义召回 | 对审批时序、身份和实体关系需额外逻辑 |
| Neo4j / FalkorDB（图数据库） | 存图、图查询、索引与持久化 | 本体、数据清洗、可信溯源和决策应用仍需自己设计 |
| DataHub / OpenMetadata（元数据平台） | 数据资产发现、目录、血缘及治理工作流 | 不等价于面向 Agent 的业务事实/决策推理层 |
| **Semantica** | 抽取、实体关系、图谱、本体、规则、决策及溯源模块集成 | 新增运维层，仍需源治理、权限和业务校验；必须压测 |

比较是架构定位，不代表上述产品一律缺少某项功能；实际应按具体版本和需求选型。

## 建议架构：行途知识资产先不换源

```text
[xingtu-vault / xingtu-learn / AGENTS.md / Git 规范与执行日志]
                          │ 只读、脱敏、增量抽取
                          ▼
          [可选的语义/关系/决策索引：Semantica]
                   │                 │
             本体与规则验证      溯源/时间与冲突处理
                   └─────┬──────────┘
                         ▼
               [Codex / Harness / FDE Agent]
                         │
           返回有来源的事实及缺失证据，绝不伪造审批
```

- 原始 Markdown/Git 仍是**事实源**；图谱是可重建的派生视图。
- 第一阶段拒绝全量同步私有 Vault、拒绝向公开仓上传内部原始数据。
- 先检索/读取，再引入验证和规则；不能从模型推理替代真实审批。
- 跨仓和多 Agent 共享先用文件/日志协议解决；出现确切的多跳查询瓶颈再上图谱。

## 部署形态与资源预算

| 形态 | 依赖/行为 | 使用建议 |
|---|---|---|
| Python 单进程 | `pip install semantica`，内存 ContextGraph，可显式导出 JSON | **首选**：无 GPU、无图数据库 |
| MCP/CLI | `semantica-mcp` / CLI 进程 | 在基础实验通过后，按需接入 Agent，勿直接开放全部工具 |
| Docker Compose | 源码 `docker-compose.yml`：`explorer`（8000）+ `falkordb`（6379），命名数据卷 | 第二阶段，验证 Explorer、持久化、重启和鉴权 |
| 私有生产部署 | 自建服务、持久化图存储、备份、权限、监控、资源隔离 | 需要额外安全设计与负载测试；不是一条命令变成合规生产 |

**起步资源预算（仅为实验规划，非官方最低配置、非实测）：**

- 小型单进程：建议预留 2 vCPU / 4 GiB RAM。
- Docker Explorer + FalkorDB：建议预留 4 vCPU / 8 GiB RAM。
- 批量抽取/更多图关系：从 4–8 vCPU、16 GiB RAM 的环境开始测，但依数据量、模型、并发而变。
- 需要记录机器芯片架构、镜像版本、工作负载、冷启动 RSS/峰值 RSS、CPU、磁盘增长与 P95，不把 `tracemalloc` 当进程真实 RSS。

**安全检查**：源码 Compose 端口映射 `8000:8000`、`6379:6379`，真实环境应限制监听地址、防火墙/内网，设置 `SEMANTICA_API_KEY`，不要在对外环境开启 `SEMANTICA_ALLOW_ANONYMOUS=true`；GraphDB 的网络入口、鉴权、备份要独立处理。仓库使用了 `latest` 图数据库镜像，生产前须固定版本。

## 商业价值：不卖一张图，卖跨系统的可核验业务上下文

1. 减少跨系统概念映射、手工核验与维护成本。
2. 给关键 AI 决策补齐依据、时间和来源，降低事故调查与审计工作量。
3. 复用行业本体、规则模板、连接器和证据处理流程，提升后续交付效率。
4. 给 FDE 提供可复用的治理方案，而不只是一次性 Chatbot。

**商业形态核查（2026-10-30）**：官网将 OSS Starter 标为免费；Pilot 为定制收费；Managed Cloud / Self-Hosted Enterprise 标注为 In Development，按官网当时页面为准。收入/客单价/企业效果暂无可独立验证数据，不臆测。开源核心 MIT 不代表企业支持服务免费。

价值计算示意：`净价值 = 节省的手工成本 + 风险预期损失降低 - 建设与持续运行成本`。必须测量真实人工耗时、正确率、漏检率和部署成本，才可判断 ROI。

## 学习与实践产物

1. [01-最小实践.md](01-最小实践.md)：先跑标准库基线，再建 ContextGraph，对照六类 FDE 需求场景。
2. [data/requirements.json](data/requirements.json)：纯合成数据，可公开复用。
3. [run_baseline.py](run_baseline.py)：确定性审批/测试规则，**非 Semantica**。
4. [run_semantica.py](run_semantica.py)：按官方 `ContextGraph` API 建图并持久化，**尚未本地运行验证**。
5. [02-评测记录模板.md](02-评测记录模板.md)：资源、正确率、漏检、能力增益和决定。
6. [03-专题选题.md](03-专题选题.md)：行途技术手记选题及论证结构。

**现阶段不做**：向公开仓上传 xingtu-vault 私有文件；改全局 Codex/CC Switch 配置；默认运行 Docker；宣称已节省 Token、符合某项法规或已达到生产稳定性。

## 一次实验的放行条件

- [ ] 6/6 合成用例判定正确，理由准确、不杜撰证据。
- [ ] 图中能查询需求→审批→测试→发布关联，保存/恢复后节点和边数量一致。
- [ ] 发现 conflicting approvals、过期审批、缺失来源，并保留来源定位。
- [ ] 对相同数据比较 Markdown/JSON+Python 与 Semantica 的真实收益和额外成本。
- [ ] 工具依赖和 API 版本明确；记录本机环境与实测 CPU/RSS/磁盘/耗时。
- [ ] 如果图谱未提供显著的多跳/溯源/跨系统能力收益，则**继续用 Markdown + JSON + Python**。

## 参考（优先官方一手资料）

- 源码与 MIT：https://github.com/semantica-agi/semantica
- ContextGraph / `save_to_file` / `record_decision`：https://docs.getsemantica.ai/reference/context/
- Getting Started：https://docs.getsemantica.ai/getting-started/
- Architecture：https://docs.getsemantica.ai/architecture/
- Performance guidance：https://docs.getsemantica.ai/learning-more/
- 当前官方价格：https://www.getsemantica.ai/pricing
- Compose/Dockerfile（以本研究时源码为准）：https://github.com/semantica-agi/semantica/blob/main/docker-compose.yml

## 研究状态

- [已审阅] 官方文档、Python 依赖、Dockerfile、Docker Compose、官网公开商业形态。
- [已编写，未实测] 基线脚本、ContextGraph 脚本、合成数据与评测模板。
- [待做] 本地依赖安装、启动、持久化实测、客观基准与正反例记录。
