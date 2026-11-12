# RepoScout 调研报告

搜索 Java Agent 项目，重点检查 langchain4j/langchain4j 最近 180 天的维护情况，说明提交与发布证据。

任务 `c7bbd1808d4b` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T15:58:16.946078+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 相关项目（最多10个候选），重点核查 langchain4j/langchain4j 在最近180天（2026-05-16 至 2026-11-12）内的维护情况，并给出提交与发布证据；深入分析1个仓库。

- Java Agent 项目（硬性条件）
- 最近180天有提交活动（硬性条件）
- 最近180天有正式发布（硬性条件）

## langchain4j/langchain4j

面向 JVM 的 Java LLM 应用库，提供统一 LLM/向量库 API、工具调用（含 MCP）、Agents 与 RAG，并集成 Quarkus、Spring Boot 等框架；仓库含独立的 langchain4j-agentic 模块，以 @Agent 注解声明可被其他 agent 调用的方法。

固定 commit `b7fe277c7437145617bcd49b77febfa5698c9ef4`

- **Java Agent 项目 · 满足**。README 明确将 Agents 列为工具箱能力，且存在 langchain4j-agentic 模块与 @Agent 注解源码。 [ev-8aeb40efc65e](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) [ev-611ceaa78eb4](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L60)
- **最近180天有提交活动 · 满足**。维护快照中最近提交日期为 2026-11-12，距今天 0 天，远在 180 天窗口内，且当日有多条提交。 [ev-bfa2e95a14c2](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- **最近180天有正式发布 · 满足**。最近发布 1.19.5 于 2026-11-02 发布（非预发布），距今天约 10 天，在 180 天窗口内。 [ev-bfa2e95a14c2](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)

**推荐**。三项条件均有直接证据满足：具备 Java Agent 能力（agentic 模块 + @Agent 注解），180 天内既有当日提交也有 2026-11-02 的正式发布。 [ev-8aeb40efc65e](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) [ev-611ceaa78eb4](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L60) [ev-bfa2e95a14c2](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) [ev-dcdc5d7c4010](https://github.com/langchain4j/langchain4j)

- README 说明工具箱覆盖从 prompt 模板、chat memory、function calling 到 Agents 与 RAG 的高层模式。（依据 `documentation`） [ev-8aeb40efc65e](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80)
- 源码中 dev.langchain4j.agentic.Agent 为 @Retention(RUNTIME)、@Target(METHOD) 的注解，被标注的 Java 方法即视为可被其他 agent 调用的 agent。（依据 `source`） [ev-611ceaa78eb4](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L60)
- 维护快照显示 2026-11-12 当天有多次提交（如 #7097 Agentic 修复、#7087 watsonx.ai SDK 升级），最近发布为 2026-11-02 的 1.19.5、1.5.4、1.19.4。（依据 `metadata`） [ev-bfa2e95a14c2](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- 仓库元数据：Apache-2.0 许可、未归档、默认分支 main、约 13.4k stars、1122 个开放 issue，pushed_at 为 2026-11-12。（依据 `metadata`） [ev-dcdc5d7c4010](https://github.com/langchain4j/langchain4j)
- 未确认项 — 未运行构建或基准测试，性能与稳定性无实测数据
- 未确认项 — 1122 个开放 issue 的实际处理节奏未逐项核查
- 未确认项 — 仅读取维护快照中的最近 5 条提交与 3 个发布，180 天内完整提交/发布总量未统计

## 结论

在 6 个 Java Agent 相关候选中（agentscope-ai/agentscope-java、bytechefhq/bytechef、langchain4j/langchain4j、Atmosphere/atmosphere、google/adk-java、agents-flex/agents-flex），按要求深入分析了 langchain4j/langchain4j：其 agentic 模块与 @Agent 注解证实 Java Agent 能力；维护方面，固定 commit b7fe277 的快照显示 2026-11-12 当日仍有多次提交，最近正式发布为 2026-11-02 的 1.19.5，180 天窗口内提交与发布证据均成立，判定推荐。其余 5 个候选仅保留为未深入分析。

## 未确认项

- 其余 5 个候选未做维护与能力核查，不能据此排除
- langchain4j 的 180 天完整提交/发布数量、issue 处理时效未统计
- 无独立部署与性能实测证据

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 1 轮 · 补证 0 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-074ae0a05a4e](https://github.com/search?q=java+agent+llm+language%3Ajava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 6 个公开候选 · 读取时间 `2026-11-12T15:51:42.129316+00:00`
- [ev-611ceaa78eb4](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L60) · langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 1 至 60 行，共 193 行 · 读取时间 `2026-11-12T15:51:48.509420+00:00` · 内容已截断
- [ev-8aeb40efc65e](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) · README.md 第 1 至 80 行，共 85 行 · 读取时间 `2026-11-12T15:51:48.931352+00:00` · 内容已截断
- [ev-bfa2e95a14c2](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T15:51:45.604540+00:00`
- [ev-dcdc5d7c4010](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T15:51:44.348245+00:00`

## 执行统计

```json
{
  "model_calls": 8,
  "input_tokens": 57641,
  "output_tokens": 3424,
  "estimated_cost_cny_upper_bound": 0.787793,
  "global_reserved_and_spent_cny": 11.530902,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": false,
  "github_requests": 7,
  "elapsed_seconds": 39.289,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 5,
      "cost_cny": 0.109778,
      "input_tokens": 45885,
      "output_tokens": 2251
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 3,
      "cost_cny": 0.678015,
      "input_tokens": 11756,
      "output_tokens": 1173
    }
  ],
  "retrieval": {}
}
```

## 异常记录

- `uncertain_usage` 模型请求中断，用量未确认，保留预留费用并停止付费调用
- `budget_acknowledged` 人工接受最高预留 0.540540 元，实际用量仍未确认
