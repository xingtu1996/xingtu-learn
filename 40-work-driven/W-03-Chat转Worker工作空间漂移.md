# W-03｜Chat 转 Worker 工作空间漂移（2026-11-03）

> 类型：工程实践踩坑 | 标签：Worker、工作空间、Codex、Harness、导航漂移
> 现象：公众号文章在错误目录下生成，色值/结构/逻辑全错，返工到 v5 才被发现

## 问题

Chat（豆包办公 / Qwen Chat）转 Worker（Codex CLI / Qwen Worker）时，
Worker 默认在 `~/Documents/Codex/YYYY-MM-DD/` 下启动，
**不会自动切到 `/Users/lijiacheng/xingtu/`**。

结果：
- Worker 没读行途 AGENTS.md
- 不知道 DESIGN.md 三原色和封面白底规则
- 不知道 publish-pack-planning 五步闸门
- 不知道叙事骨架 Step 0.5
- 产出色值漂移、结构混乱、逻辑同平面罗列

## 根因

Chat 宿主把项目规则作为系统提示强制注入；
Worker（CLI）是文件读取式，**启动时只看 cwd 下的 AGENTS.md**。
如果 cwd 不是 `/Users/lijiacheng/xingtu/`，就等于零行途上下文。

## 解决（三层防护）

### 第一层：Worker 默认工作区放指路牌

`~/Documents/Codex/AGENTS.md` 写"你走错了，去 /Users/lijiacheng/xingtu/"。
Worker 启动读 cwd AGENTS.md 时会被拦住。

### 第二层：Chat 转 Worker 提示词模板

见 `W-03-worker-onboard-prompt.md`（同目录）。
Chat 转 Worker 时把这段提示词贴给 Worker，强制 cd + 读 AGENTS.md。

### 第三层：全局 Codex 配置指针

`~/.codex/AGENTS.md` 末尾加行途项目指针（已完成，2026-11-03）。

## 可复用结论

1. **Worker 启动第一件事是确认 cwd**——不是读文件，是先 `pwd` 看对不对
2. **Chat→Worker 转换不是无缝的**——宿主变了，上下文装载机制变了
3. **默认工作区必须放指路牌**——这是最低成本的防呆
4. **产出不对时先查工作空间**——比查模型/查 skill 更快定位

## 关联

- W-02：Codex-Harness 智能路由实验
- DESIGN.md §八·补：叙事骨架指针
- publish-pack-planning Step 0.5：叙事骨架闸门
