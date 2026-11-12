# RepoScout 调研报告

搜索 Java Agent 框架，检查 langchain4j/langchain4j 是否有可证明单机 1 万 QPS 的独立基准，资料不足时明确未确认。

任务 `747fcdb5bd3e` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T10:12:29.972458+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 框架候选，重点核查 langchain4j/langchain4j 是否存在可证明单机 1 万 QPS 的独立基准；资料不足时明确标注未确认。

- Java Agent 框架（硬性条件）
- 存在可证明单机 1 万 QPS 的独立基准（硬性条件）

## langchain4j/langchain4j

LangChain4j 是面向 JVM 的 Java LLM 应用库，提供统一 API、工具调用、Agents 与 RAG，并含 agentic 相关模块；仓库活跃维护。但本次读取的材料中未发现任何 QPS/吞吐基准，1 万 QPS 无法确认。

固定 commit `fb6e252b7a67e0d0579957127cafea9202ba1019`

- **Java Agent 框架 · 满足**。README 明确提供 Agents 等高层模式，pom 中存在 langchain4j-agentic 系列模块。 [ev-ed80b2610711](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) [ev-afa99e14b03b](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L60-L199)
- **存在可证明单机 1 万 QPS 的独立基准 · 未确认**。已读 README 与聚合 pom 均未提及任何 QPS/吞吐基准或性能测试模块；未找到可引用的独立基准数据。 [ev-ed80b2610711](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) [ev-afa99e14b03b](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L60-L199) [ev-3dd1c25380d1](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L200-L321)

**待确认**。Agent 框架属性可确认，但单机 1 万 QPS 的独立基准在已读材料中无任何证据，需补充基准数据后再定。 [ev-ed80b2610711](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) [ev-afa99e14b03b](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L60-L199) [ev-6da1c7e31c5e](https://github.com/langchain4j/langchain4j) [ev-562a2c1ccdad](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)

- README 自述为 JVM 上构建 LLM 应用的 Java 库，工具箱含 Agents、RAG、函数调用等高层模式。（依据 `documentation`） [ev-ed80b2610711](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80)
- 聚合 pom 含 langchain4j-agentic、agentic-a2a、agentic-mcp、agentic-patterns、skills 等模块，说明具备 Agent 相关实现。（依据 `source`） [ev-afa99e14b03b](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L60-L199)
- 元数据：Apache-2.0，13394 stars，未归档；最近提交 2026-11-12，最近发布 1.19.5（2026-11-02），维护活跃。（依据 `metadata`） [ev-6da1c7e31c5e](https://github.com/langchain4j/langchain4j) [ev-562a2c1ccdad](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)
- 未确认项 — 仓库内是否存在 JMH/压测模块或性能文档（未检索到）
- 未确认项 — 任何单机 QPS 实测数据与测试环境配置
- 未确认项 — LLM 调用受外部服务延迟约束，框架层 QPS 上限未实测

## 结论

搜索到 2 个 Java Agent 框架候选：langchain4j/langchain4j（13394 stars）与 agents-flex/agents-flex（1054 stars，未深入分析）。对 langchain4j 固定 commit fb6e252 核查后：其 Agent 能力可确认（README 与 agentic 模块），维护活跃（2026-11-12 有提交、2026-11-02 发布 1.19.5）。但关于“单机 1 万 QPS 的独立基准”，已读 README、聚合 pom 中均无任何基准或性能测试证据，结论为未确认，不能宣称其满足该指标。

## 未确认项

- langchain4j 是否存在独立压测仓库或第三方基准报告
- agents-flex 未做深入分析，其性能数据同样未确认

## 证据索引

- [ev-3dd1c25380d1](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L200-L321) · pom.xml 第 200 至 321 行，共 321 行 · 读取时间 `2026-11-12T10:12:19.519964+00:00` · 内容已截断
- [ev-562a2c1ccdad](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T10:12:13.778208+00:00`
- [ev-651545a7385d](https://github.com/search?q=java+agent+framework+llm+language%3AJava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 2 个公开候选 · 读取时间 `2026-11-12T10:12:12.116028+00:00`
- [ev-6da1c7e31c5e](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T10:12:12.757062+00:00`
- [ev-afa99e14b03b](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L60-L199) · pom.xml 第 60 至 199 行，共 321 行 · 读取时间 `2026-11-12T10:12:20.957574+00:00` · 内容已截断
- [ev-e83c79ed01d7](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L1-L60) · pom.xml 第 1 至 60 行，共 321 行 · 读取时间 `2026-11-12T10:12:17.915772+00:00` · 内容已截断
- [ev-ed80b2610711](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) · README.md 第 1 至 80 行，共 85 行 · 读取时间 `2026-11-12T10:12:17.894956+00:00` · 内容已截断

## 执行统计

```json
{
  "model_calls": 9,
  "input_tokens": 94462,
  "output_tokens": 2093,
  "estimated_cost_cny_upper_bound": 0.205668,
  "global_reserved_and_spent_cny": 9.887948,
  "unconfirmed_calls": 0,
  "github_requests": 8,
  "elapsed_seconds": 20.753
}
```

## 异常记录

- `response_too_large` GitHub 响应超过 2 MB 限制
