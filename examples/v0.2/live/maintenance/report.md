# RepoScout 调研报告

搜索 Java Agent 项目，重点检查 langchain4j/langchain4j 最近 180 天的维护情况，说明提交与发布证据。

任务 `44ea217a174b` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T16:23:41.009336+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 相关项目，重点核查 langchain4j/langchain4j 最近 180 天（2026-05-16 至 2026-11-12）的维护情况，并给出提交与发布证据。搜索上限 10 个候选，深入分析 1 个。

- Java Agent 项目（硬性条件）
- 最近 180 天有提交（硬性条件）
- 最近 180 天有发布（硬性条件）

## langchain4j/langchain4j

JVM 上的 Java LLM 应用库，提供统一 LLM/向量库 API，并含 agentic 模块（@Agent 注解、AgenticScope 等）。固定 commit b7fe277c7437145617bcd49b77febfa5698c9ef4，Apache-2.0，13.4k stars，未归档。

固定 commit `b7fe277c7437145617bcd49b77febfa5698c9ef4`

- **Java Agent 项目 · 满足**。仓库为 Java 库，README 明确将 Agents 列为工具箱高层模式，且存在 langchain4j-agentic 模块的 @Agent 注解源码。 [ev-c4f32a51f6a9](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) [ev-83674fb763d3](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-e78f6b986a37](https://github.com/langchain4j/langchain4j)
- **最近 180 天有提交 · 满足**。最近提交日期为 2026-11-12，距今天 0 天，远在 180 天窗口内；pushed_at 同为 2026-11-12。 [ev-04abc7d0a31b](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) [ev-e78f6b986a37](https://github.com/langchain4j/langchain4j)
- **最近 180 天有发布 · 满足**。最近正式发布 1.19.5 于 2026-11-02，距今天约 10 天，在 180 天窗口内。 [ev-04abc7d0a31b](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)

**推荐**。三项硬性条件均有证据满足：Java 语言且具备 agentic 能力，最近提交（2026-11-12）与最近发布（2026-11-02）均在 180 天窗口内，维护活跃。 [ev-e78f6b986a37](https://github.com/langchain4j/langchain4j) [ev-04abc7d0a31b](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) [ev-c4f32a51f6a9](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) [ev-83674fb763d3](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80)

- 仓库元数据：Java 语言、Apache-2.0、13393 stars、未归档未禁用，pushed_at 为 2026-11-12T15:25:46Z。（依据 `metadata`） [ev-e78f6b986a37](https://github.com/langchain4j/langchain4j)
- 最近提交集中在 2026-11-12，含 Agentic 异步 agent 挂起通知修复（#7097）、watsonx.ai SDK 升级（#7087）、CI Maven 缓存（#7094）等。（依据 `metadata`） [ev-04abc7d0a31b](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- 最近发布为 1.19.5（2026-11-02）、1.5.4 与 1.19.4（均 2026-11-02），均为正式版。（依据 `metadata`） [ev-04abc7d0a31b](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- README 说明其工具箱覆盖从 prompt 模板、chat memory、function calling 到 Agents 与 RAG 的高层模式。（依据 `documentation`） [ev-c4f32a51f6a9](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80)
- 源码中 dev.langchain4j.agentic.Agent 为方法级注解，标注的方法被视为可被其他 agent 调用的 agent，支持 name/description/outputKey/typedOutputKey 等属性。（依据 `source`） [ev-83674fb763d3](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80)
- 未确认项 — 未统计 180 天内提交总数与发布总数，仅依据最近若干条快照
- 未确认项 — 未实测 agentic 模块运行效果与性能
- 未确认项 — 未评估 1122 个 open issues 的响应时效

## 结论

在 3 个搜索候选中（langchain4j/langchain4j、JetBrains/koog、agents-flex/agents-flex），仅深入分析用户点名的 langchain4j/langchain4j。该仓库为 Java 生态的 LLM/Agent 库，最近 180 天维护活跃：最近提交 2026-11-12（含 Agentic 相关修复），最近正式发布 1.19.5 于 2026-11-02，满足全部硬性条件，推荐作为 Java Agent 技术选型候选。其余两个候选仅保留为未深入分析。

## 未确认项

- 未统计 180 天内提交与发布的总量趋势
- 未实测运行效果、性能与稳定性
- 未评估 issue 响应时效与社区支持质量

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 1 轮 · 补证 0 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-04abc7d0a31b](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:01:31.049285+00:00`
- [ev-83674fb763d3](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) · langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 1 至 80 行，共 193 行 · 读取时间 `2026-11-12T16:01:33.466044+00:00` · 内容已截断
- [ev-c4f32a51f6a9](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) · README.md 第 1 至 80 行，共 85 行 · 读取时间 `2026-11-12T16:01:33.466271+00:00` · 内容已截断
- [ev-d178898a4c94](https://github.com/search?q=java+agent+llm+framework+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 3 个公开候选 · 读取时间 `2026-11-12T16:01:29.312333+00:00`
- [ev-e78f6b986a37](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:01:29.821870+00:00`

## 执行统计

```json
{
  "model_calls": 6,
  "input_tokens": 51110,
  "output_tokens": 3531,
  "estimated_cost_cny_upper_bound": 0.240648,
  "global_reserved_and_spent_cny": 13.926723,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": true,
  "run_unconfirmed_calls": 0,
  "github_requests": 7,
  "elapsed_seconds": 38.236,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 4,
      "cost_cny": 0.095676,
      "input_tokens": 38866,
      "output_tokens": 2243
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 2,
      "cost_cny": 0.144972,
      "input_tokens": 12244,
      "output_tokens": 1288
    }
  ],
  "retrieval": {}
}
```
