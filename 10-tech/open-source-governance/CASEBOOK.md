# 行途真实案例｜开源授权、内容版权与工程治理

> 快照：2026-11-03；仅引用可公开访问的仓库文件。**这是学习审计样例，不代表已完成法律审查或 PR 已合并。** 不讨论私有仓库的具体源文件或内部信息。  
> [专题首页](README.md) · [核对清单](CHECKLIST.md)

## 案例 1｜`xingtu-articles`：README 声称 CC BY-SA，LICENSE 实际为 MIT

- **公开证据 A**： [`README.md`](https://github.com/xingtu1996/xingtu-articles/blob/main/README.md) 的徽章、License 小节写文章内容采用 `CC BY-SA 4.0`。
- **公开证据 B**： [`LICENSE`](https://github.com/xingtu1996/xingtu-articles/blob/main/LICENSE) 当前实际正文是 `MIT License`。
- **问题**：根文件、README、徽章对权利授予范围的声明不一致。不能从单一徽章或自动识别状态推断文章已统一得到 CC BY-SA 授权；也不能不经原版权人的批准直接覆盖许可证。
- **风险**：下游复用者可能误认为文章、配图与代码统一适用某个许可；图片可能有第三方独立权利。
- **最低处理方案（待审，不修改原仓）**：
  1. 先列出资产清单：原创正文、第三方引用、封面配图、排版/程序代码。
  2. 由实际权利人确认各层许可；明确例如 `content/`、`code/`、`assets/` 的边界，必要时使用 `LICENSES/` 与 `THIRD_PARTY_NOTICES`。
  3. 一次性对齐主许可证、README、徽章、文件头和历史版本说明，并让独立 reviewer 核对。
  4. 已传播历史版本和下游用户的既有授权不能依靠“修改新文件”简单撤回。

**本案例当前结论：`LICENSE_CONFLICT / 暂缓声称已经统一完成 CC BY-SA 授权`**。没有自动修改仓库授权。

## 案例 2｜`xingtu-fde`：可公开阅读 ≠ 已获得开源再分发许可

- **证据**： [`xingtu-fde/LICENSE.md`](https://github.com/xingtu1996/xingtu-fde/blob/main/LICENSE.md) 明确说明许可证待裁决、尚未授予统一再分发权。
- **事实边界**：公开仓已存在不代表全部资产可自由再授权。草稿 PR 含模板、第三方案例和引用材料时，权属还需要逐项审阅。
- **建议**：知识卡、案例、Skill 链接、第三方来源分别列权利字段；正式授权前不做“随意商用/可自由复制”的承诺。纯源码未来采用 MIT 与内容采用 CC BY-SA 只是候选分层设计，需权利人裁决。
- **当前结论**：`RIGHTS_UNDECIDED / 公开阅读可用，但不得自动宣称已完成开源许可治理`。

## 案例 3｜MIT 与 Apache-2.0 并存：矩阵统一，不等于许可证统一

- [`xingtu-harness`](https://github.com/xingtu1996/xingtu-harness) 与多个工具库使用 MIT。
- [`harness-kit`](https://github.com/xingtu1996/harness-kit) 使用 Apache-2.0，且有 `NOTICE` 等文件。
- **学习点**：同一个开源生态下不同仓库可以合理采用不同许可证。矩阵的统一目标是让项目权利**清楚、一致、可检索**，不是把所有 LICENSE 改成 MIT。
- **行动**：建立仓库分类、权属与 SPDX 映射；跨仓复用代码时保留每份上游许可证、NOTICE 与修改记录；发布聚合包时重新审查集成后的义务。

## 案例 4｜“升级依赖”与“发布新版本”不能打包放行

假设一个本地工具的依赖触发 GHSA/CVE 警报，这是**合成情境**，不是声称上述仓库已存在漏洞。

- **误做法**：看到 Dependabot PR 就全自动合并并发版。
- **正确做法**：确认受影响范围、受害条件、升级目标；对照改动后的许可证与 NOTICE；运行测试、准备回滚；有权限的人员批准后才部署。
- **验证字段**：`advisory_id`、`affected_version`、`patched_version`、`runtime_exposure`、`license_before`、`license_after`、`tests`、`reviewer`、`rollback_sha`。
- **结论**：安全工具提出的是风险和修复候选，不能替代兼容审查、授权审查与运行测试。

## 可用于本轮仓库治理的建议

1. 对所有公开仓做**只读**的 `LICENSE / README 声明 / GitHub 识别 / SPDX` 对账，形成冲突列表，而非立即批量重授权。
2. 各仓先完成中文 `README.md` 为主、`README.en.md` 为英文入口；按真实成熟度标注设计、实验、验证及生产。
3. 公开知识与代码按资产权利分层；第三方转载只引用链接及合理必要摘要，不搬运全文。
4. 对企业项目与个人项目**分开治理**，避免把带有公司权利限制的素材放到公开仓。
5. 以 [CHECKLIST.md](CHECKLIST.md) 作为新人学习与 PR Reviewer 的检查起点；真实修改另建有权限、可回滚的 PR。

## 证据等级与待验证项

- `observed`：已读取所链接公开仓的文件，确认上述不一致与待裁决陈述。
- `not_verified`：许可证法务意见、贡献者授权链、历史版本对外再授权事实、第三方素材全量清单、上游依赖许可兼容性。
- `not_performed`：未修改原仓 LICENSE、未合并相关 Draft PR、未触发生产发布。

注意：GitHub 页面会随分支变更；执行前须固化目标 commit SHA，并重读当前许可证。此处链接到主分支作为学习入口，而非不可变审计证据。

