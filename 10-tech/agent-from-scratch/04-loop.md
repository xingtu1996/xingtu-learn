> status: 活跃 ｜ 更新: 2026-09-13 ｜ 来源: PEC2026 梁凯锐（词元映射 tokenmap CTO）+ 个人重建
> 现场源码：https://github.com/tokenmapai/start-anew-agent （stage 02 / 06 / 07）

# 04 · 循环：while 循环与 Skill 渐进加载

## ① 这一层解决什么问题

前三篇拼出了「有工具、会推理」的 Agent，但还卡在一个死结：你写死一次工具调用，它就只能做一步。可真实任务是一串的——查日历之后要订票，订票之后要订酒店，订酒店之后要租车……按场景硬写，代码会无穷无尽。

解法是把重复的工具执行抽成一个 while 循环。循环体每次都是同一段「模型请求 → 程序执行 → 结果写回」，外加一个出口判断：当模型说「我够了，这是最终答案」，就停。这一行 while，把「什么时候走下一步」的决策权，从程序手里挪到了模型手里。到这一步，Agent 才真正立起来。

但循环一开，Skill 多了又会压垮上下文窗口——几百个 Skill 全塞进去，token 爆掉。于是有了渐进式加载：平时只留一个查询入口，模型用到哪个 Skill 再加载哪个。

## ② 最小代码：五版进化（高潮在 V3/V5）

```python
# V1 两行 / V2 五行：见 01、03，单轮，做不了多步任务

# V3 while True：决策权从程序挪到模型
ctx = system_prompt + user_input + tool_protocol + tool_set
while True:
    step = model(ctx)
    if step.is_final_answer:          # 出口判断：模型自己说停
        break
    ctx = append_context(ctx, run_tool(step))   # 同一段执行，可无限次
print(ctx.final_answer)

# V5 skill_catalog：Skill 渐进式加载
skill_protocol = [{"name": "book_trip", "solves": "差旅全流程", "input": "..."}]  # 几百个也只放目录

def search_skill(query): ...          # 只花一个 search 协议的 token
def load_skill(name):
    md = read(f"skills/{name}.md")     # Skill 是 markdown 文档
    ctx = append_context(ctx, md)      # 按需把正文加载进上下文
```

V3 让 Agent 「活」了；V5 让成百上千个 Skill 不至于撑爆窗口。两者合起来，就是梁凯锐说的「Agent 的始末」。

## ③ 现场原话转述

> 梁凯锐@PEC2026：加一个 while 循环——执行工具没变、任务难度没变，但决策权从程序挪到了模型，真正实现了 ReAct 那四个节点：让模型去观察、判断下一步、程序承接执行、结果再返回模型。Skill 最终是一份 .md 文档，内容会加载进上下文；如果几百个 Skill 全放上下文窗口，压力会非常大，所以优化做法是把它移出上下文，只给模型一个查询方式，这样只多花一个 search_skill 的协议 token，就能让模型去查库里已有的几百个技能。

（转述现场要点，非逐字原文）

## ④ 我的理解

这一篇是把我上午场两个原创判断一次性验明正身的地方：

- 「本质模型控制，其他皆 Harness」——while 循环那一行，就是把「下一步怎么走」交还给模型，这正是把控制权留在模型、其余（循环、协议、加载）全算 Harness 的工程注脚。
- 「把 Harness 封装成 Skills」——V5 的 search/load_skill 就是这句话的落地：每一种控制手段沉淀成一个可复用 Skill，用到才加载。

我上午先想到，下午被整场连续验证。现场还有个形象说法：对话是「点」，工具调用和上下文是「线」，Agent 自主决定用不用工具、何时停，就是「圈」。这个点→线→圈，正好就是这条学习线四篇的收口。

## ⑤ 可复用产物：Skill 渐进加载骨架

```python
# 上下文里只留这一行协议，其余 Skill 不预载
ctx += {"skill_search": "传入关键词，返回匹配的 Skill 名称"}

def handle(model_step):
    if model_step.tool == "search_skill":
        return list_skills(model_step.query)          # 轻量，省 token
    if model_step.tool == "load_skill":
        md = read(f"skills/{model_step.name}.md")
        return append_context(ctx, md)                # 按需加载正文
```

命名规范：`skills/<name>.md` 每份只讲「这个 Skill 解决什么、按什么步骤做」，让模型照着工作，而不是替它跑代码。

## ⑥ 待验证 / 我不确定的地方

- 「几百个 Skill 只花 1 个 search token」是现场说法，标签待核实：真实省下的量取决于协议写法，我还没在自己环境测过。
- 现场另一位做个人 AI 工作流的分享者提到：Skill 多了会「打架」——它们被预加载进上下文后相互冲突。解法他给了两条：关掉无关 Skill、把一组 Skill 打包成工作流插件。这套冲突治理我没实践过，标待验证。
- 60 分的 Skill 容易做、好用的 Skill 难（他说内部改了 100 多版也就到七八十分）。这条我认同但没亲历，准备拿自己的素材处理助手试一轮。
