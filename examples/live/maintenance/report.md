# RepoScout 调研报告

搜索 Java Agent 项目，重点检查 langchain4j/langchain4j 最近 180 天的维护情况，说明提交与发布证据。

任务 `1a4e85495217` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T10:10:41.416793+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 项目，重点核查 langchain4j/langchain4j 最近 180 天（2026-05-16 至 2026-11-12）的维护情况，并给出提交与发布证据。

- Java Agent 项目（硬性条件）
- 最近 180 天有维护活动（提交与发布）（硬性条件）

## langchain4j/langchain4j

面向 JVM 的 Java LLM 应用库，提供统一 API、工具调用（含 MCP）、Agents 与 RAG 等能力；固定 commit fb6e252，Apache-2.0，13.4k stars。

固定 commit `fb6e252b7a67e0d0579957127cafea9202ba1019`

- **Java Agent 项目 · 满足**。README 明确将 Agents 列为工具箱中的高层模式，仓库语言为 Java。 [ev-c37b6784bc80](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) [ev-89375d8ef3cd](https://github.com/langchain4j/langchain4j)
- **最近 180 天有维护活动（提交与发布） · 满足**。最近提交为 2026-11-12（含依赖升级 PR #7081、#7098 等），最近发布 1.19.5 于 2026-11-02，均在 180 天窗口内。 [ev-daa199a23f3b](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)

**推荐**。Agent 能力有 README 文档支撑，且 180 天窗口内提交与发布证据齐全，维护活跃。 [ev-c37b6784bc80](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) [ev-89375d8ef3cd](https://github.com/langchain4j/langchain4j) [ev-daa199a23f3b](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)

- README 称工具箱覆盖从 prompt 模板、chat memory、function calling 到 Agents 与 RAG 的高层模式。（依据 `documentation`） [ev-c37b6784bc80](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80)
- README 声明支持 20+ LLM 提供商与 30+ embedding store，并可与 Quarkus、Spring Boot、Helidon、Micronaut 集成。（依据 `documentation`） [ev-c37b6784bc80](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80)
- 元数据：Apache-2.0 许可，未归档，默认分支 main，open issues 1120，pushed_at 2026-11-12。（依据 `metadata`） [ev-89375d8ef3cd](https://github.com/langchain4j/langchain4j)
- 未确认项 — 未运行代码，实际 Agent 编排效果与性能无实测
- 未确认项 — 未核查 issue 响应时长与贡献者集中度

## 结论

搜索得到 6 个 Java Agent 候选（langchain4j、agentscope-java、atmosphere、bytechef、google/adk-java、agents-flex），仅深入分析 langchain4j/langchain4j：其 README 明确支持 Agents，最近提交 2026-11-12、最近发布 1.19.5（2026-11-02），180 天内维护活跃，推荐作为 Java Agent 技术选型候选；其余候选未深入分析。

## 未确认项

- 其余 5 个候选的维护与 Agent 能力未核实
- langchain4j 的运行时性能与生产稳定性无基准证据

## 证据索引

- [ev-371af4e791c9](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L80-L85) · README.md 第 80 至 85 行，共 85 行 · 读取时间 `2026-11-12T10:10:32.196517+00:00` · 内容已截断
- [ev-54648e0de821](https://github.com/search?q=java+agent+llm+language%3AJava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 6 个公开候选 · 读取时间 `2026-11-12T10:10:25.019907+00:00`
- [ev-89375d8ef3cd](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T10:10:25.475416+00:00`
- [ev-c37b6784bc80](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L80) · README.md 第 1 至 80 行，共 85 行 · 读取时间 `2026-11-12T10:10:30.960388+00:00` · 内容已截断
- [ev-daa199a23f3b](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T10:10:26.695346+00:00`

## 执行统计

```json
{
  "model_calls": 8,
  "input_tokens": 69942,
  "output_tokens": 2088,
  "estimated_cost_cny_upper_bound": 0.156588,
  "global_reserved_and_spent_cny": 9.213928,
  "unconfirmed_calls": 0,
  "github_requests": 7,
  "elapsed_seconds": 20.37
}
```

## 异常记录

- `response_too_large` GitHub 响应超过 2 MB 限制
