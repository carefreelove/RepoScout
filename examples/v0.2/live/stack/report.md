# RepoScout 调研报告

搜索支持 Java 的开源 LLM Agent 框架，重点调研 langchain4j/langchain4j，给出依赖或源码依据。

任务 `9609c46d1b2b` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T16:23:41.003550+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索支持 Java 的开源 LLM Agent 框架，重点调研 langchain4j/langchain4j，并给出依赖（Maven 模块/pom）或源码层面的依据。

- 开源（有开源许可证）（硬性条件）
- 支持 Java 语言（硬性条件）
- 提供 LLM Agent 能力（硬性条件）

## langchain4j/langchain4j

LangChain4j 是面向 JVM 的 Java LLM 应用库，仓库以 Maven 多模块聚合工程组织，包含 langchain4j-agentic、langchain4j-agentic-a2a、langchain4j-agentic-mcp、langchain4j-agentic-patterns 等 Agent 相关模块；Agent.java 定义了 @Agent 注解，支持异步、可选、补偿与上下文摘要等 Agent 语义。

固定 commit `b7fe277c7437145617bcd49b77febfa5698c9ef4`

- **开源（有开源许可证） · 满足**。仓库元数据显示 license 为 Apache License 2.0，且未归档、未禁用。 [ev-9d5a5e105e08](https://github.com/langchain4j/langchain4j)
- **支持 Java 语言 · 满足**。元数据 language 为 Java；根 pom.xml 为 Maven 工程，Agent.java 为 Java 源码并定义 Java 注解。 [ev-9d5a5e105e08](https://github.com/langchain4j/langchain4j) [ev-a1f7950a51e6](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L1-L80) [ev-623b2d052ef1](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80)
- **提供 LLM Agent 能力 · 满足**。pom.xml 列出 langchain4j-agentic 等 Agent 模块；Agent.java 的 @Agent 注解文档说明被注解的 Java 方法即为可被其他 Agent 调用的 Agent，并支持 async、optional、compensateOnError、summarizedContext。 [ev-63de4bc98e04](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150) [ev-623b2d052ef1](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-271fc4128e82](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L141-L193)

**推荐**。三项条件均有源码/元数据证据支持：Apache-2.0 开源、Java 语言与 Maven 模块化依赖、langchain4j-agentic 模块及 @Agent 注解提供 Agent 能力；维护活跃（2026-11-12 有提交，2026-11-02 有发布）。 [ev-9d5a5e105e08](https://github.com/langchain4j/langchain4j) [ev-a1f7950a51e6](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L1-L80) [ev-63de4bc98e04](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150) [ev-623b2d052ef1](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-271fc4128e82](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L141-L193) [ev-2825329b8931](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)

- 根 pom.xml 声明 groupId dev.langchain4j、artifactId langchain4j-aggregator、packaging pom，版本 1.24.0-beta34-SNAPSHOT，是 Maven 多模块工程。（依据 `source`） [ev-a1f7950a51e6](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L1-L80)
- pom.xml 的 modules 列表包含 langchain4j-agentic、langchain4j-agentic-a2a、langchain4j-agentic-mcp、langchain4j-agentic-patterns（位于 experimental 注释段之后）。（依据 `source`） [ev-63de4bc98e04](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150)
- Agent.java 定义 @Agent 注解（@Target(METHOD)、@Retention(RUNTIME)），含 name/description/outputKey/typedOutputKey/async/optional/compensateOnError/summarizedContext 等属性。（依据 `source`） [ev-623b2d052ef1](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-271fc4128e82](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L141-L193)
- 仓库元数据：语言 Java，Apache-2.0 许可证，未归档，stars 13393，最近提交 2026-11-12，最近发布 1.19.5（2026-11-02）。（依据 `metadata`） [ev-9d5a5e105e08](https://github.com/langchain4j/langchain4j) [ev-2825329b8931](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- 未确认项 — 未读取 langchain4j-agentic 模块自身的 pom.xml，其具体 artifactId 与依赖坐标未确认。
- 未确认项 — 未运行框架，实际 Agent 编排效果与性能无实测证据。
- 未确认项 — Agent 模块在 pom 中位于 experimental 注释段之后，其稳定性/API 兼容性承诺未确认。

## 结论

在本次搜索（java llm agent framework language:java stars:>1000）返回的 2 个候选中，langchain4j/langchain4j 经源码与元数据核验满足“开源、支持 Java、提供 LLM Agent 能力”三项条件，推荐作为 Java 技术栈的 LLM Agent 框架候选。依赖依据：根 pom.xml 为 Maven 多模块工程并列出 langchain4j-agentic、langchain4j-agentic-a2a、langchain4j-agentic-mcp、langchain4j-agentic-patterns 模块；源码依据：langchain4j-agentic 中 Agent.java 定义 @Agent 注解及 async/optional/compensateOnError/summarizedContext 等 Agent 语义。另一候选 agents-flex/agents-flex 仅出现在搜索结果中，未深入分析，不作结论。

## 未确认项

- langchain4j-agentic 模块的具体 Maven 坐标（artifactId/依赖声明）未读取确认。
- 未进行实际部署与性能测试。
- agents-flex/agents-flex 未深入分析。

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 1 轮 · 补证 0 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-210a2b6d0109](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) · 全文检索命中 langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 1 至 80 行 · 读取时间 `2026-11-12T15:50:59.131625+00:00`
- [ev-271fc4128e82](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L141-L193) · 全文检索命中 langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 141 至 193 行 · 读取时间 `2026-11-12T15:50:59.131625+00:00`
- [ev-2825329b8931](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:00:37.160747+00:00`
- [ev-362c2f99bf2e](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L240-L321) · pom.xml 第 240 至 321 行，共 321 行 · 读取时间 `2026-11-12T16:00:41.154456+00:00` · 内容已截断
- [ev-623b2d052ef1](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) · langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 1 至 80 行，共 193 行 · 读取时间 `2026-11-12T16:00:39.473968+00:00` · 内容已截断
- [ev-63de4bc98e04](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150) · 全文检索命中 pom.xml 第 71 至 150 行 · 读取时间 `2026-11-12T15:48:12.394333+00:00`
- [ev-7d1bd8147f82](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L71-L150) · 全文检索命中 langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 71 至 150 行 · 读取时间 `2026-11-12T15:50:59.131625+00:00`
- [ev-90edf9e59097](https://github.com/search?q=java+llm+agent+framework+language%3Ajava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 2 个公开候选 · 读取时间 `2026-11-12T16:00:34.714465+00:00`
- [ev-9d5a5e105e08](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:00:35.912610+00:00`
- [ev-a1f7950a51e6](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L1-L80) · pom.xml 第 1 至 80 行，共 321 行 · 读取时间 `2026-11-12T16:00:39.465099+00:00` · 内容已截断

## 执行统计

```json
{
  "model_calls": 8,
  "input_tokens": 77283,
  "output_tokens": 4019,
  "estimated_cost_cny_upper_bound": 0.330654,
  "global_reserved_and_spent_cny": 13.926723,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": true,
  "run_unconfirmed_calls": 0,
  "github_requests": 7,
  "elapsed_seconds": 43.588,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 6,
      "cost_cny": 0.14187,
      "input_tokens": 60651,
      "output_tokens": 2571
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 2,
      "cost_cny": 0.188784,
      "input_tokens": 16632,
      "output_tokens": 1448
    }
  ],
  "retrieval": {
    "queries": 1,
    "returned_bytes": 12847,
    "seconds": 0.017395
  }
}
```

## 异常记录

- `retrieval` {"repository": "langchain4j/langchain4j", "query": "agentic", "hits": 4, "bytes": 12847}
