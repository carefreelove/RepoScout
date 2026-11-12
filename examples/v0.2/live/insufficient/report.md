# RepoScout 调研报告

搜索 Java Agent 框架，检查 langchain4j/langchain4j 是否有可证明单机 1 万 QPS 的独立基准，资料不足时明确未确认。

任务 `7da2e3c99b51` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T16:23:41.025245+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 框架候选；重点核查 langchain4j/langchain4j 是否存在可证明单机 1 万 QPS 的独立基准测试；资料不足时明确标注未确认。

- Java Agent 框架（硬性条件）
- 存在可证明单机 1 万 QPS 的独立基准（硬性条件）

## langchain4j/langchain4j

Java 生态主流 LLM 应用库，含 agentic 模块（@Agent 注解、异步 agent 等），Apache-2.0，活跃维护。仓库内未发现 bench/perf 命名的基准目录，也未检索到性能基准相关文本，无法证明单机 1 万 QPS。

固定 commit `b7fe277c7437145617bcd49b77febfa5698c9ef4`

- **Java Agent 框架 · 满足**。README 明确工具箱包含 Agents，且存在 langchain4j-agentic 模块与 @Agent 注解。 [ev-82bceb1d4b2b](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) [ev-7ef0d238786f](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-30d6443900eb](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150)
- **存在可证明单机 1 万 QPS 的独立基准 · 未确认**。根目录无 bench/perf 命名条目，已采集文本检索 performance 零命中；未读到任何 QPS 或吞吐基准数据。零命中不能证明不存在，但当前无证据支持 1 万 QPS。 [ev-742942de347b](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) [ev-9a359596b22c](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/)

**待确认**。满足 Java Agent 框架条件且维护活跃，但单机 1 万 QPS 的独立基准在已采集范围内无任何证据，需补充基准或压测资料后再定。 [ev-82bceb1d4b2b](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) [ev-7ef0d238786f](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-742942de347b](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) [ev-9a359596b22c](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) [ev-d0515d811308](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) [ev-347ae4770196](https://github.com/langchain4j/langchain4j)

- 仓库定位为 JVM 上的 LLM 应用库，工具箱包含 Agents 与 RAG 等高层模式。（依据 `documentation`） [ev-82bceb1d4b2b](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80)
- 存在 langchain4j-agentic 模块，@Agent 注解支持异步调用（async）、可选跳过、补偿等属性。（依据 `source`） [ev-7ef0d238786f](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-d580cf7d3a37](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L141-L193) [ev-30d6443900eb](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150)
- 根目录按 *bench* 与 *perf* 过滤均无匹配项；已采集文本中检索 performance 零命中。（依据 `source`） [ev-742942de347b](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) [ev-9a359596b22c](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/)
- 维护活跃：最近提交为 2026-11-12，最新 release 1.19.5 发布于 2026-11-02，Apache-2.0，约 13.4k stars。（依据 `metadata`） [ev-d0515d811308](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) [ev-347ae4770196](https://github.com/langchain4j/langchain4j)
- 未确认项 — 是否存在未以 bench/perf 命名的基准模块或文档（如 docs 站点、CI 压测任务）
- 未确认项 — 单机吞吐/QPS 实测数据完全缺失
- 未确认项 — LLM 调用场景下 QPS 受外部模型服务限制，框架自身吞吐未测

## 结论

langchain4j/langchain4j 可确认为 Java Agent 框架（agentic 模块 + @Agent 注解），维护活跃（2026-11-12 有提交，1.19.5 于 2026-11-02 发布）。但关于“单机 1 万 QPS 的独立基准”：根目录无 bench/perf 命名条目，已采集文本检索 performance 零命中，未发现任何 QPS/吞吐基准数据，因此该条件判定为未确认，不能宣称其具备可证明的 1 万 QPS 能力。搜索另命中 spring-ai-alibaba、agents-flex、EnterpriseAgentFramework 等候选，但本次分析仓库数量已达上限，未能 inspect，均未深入分析。

## 未确认项

- langchain4j 是否存在未以 bench/perf 命名的基准或压测文档
- 所有候选的单机吞吐实测数据均缺失
- spring-ai-alibaba、agents-flex、EnterpriseAgentFramework 因分析限额未 inspect

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 1 轮 · 补证 0 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-13c25badd429](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) · 目录 /，文件名匹配 *，展示偏移 0 后最多200项 · 读取时间 `2026-11-12T16:04:16.282324+00:00`
- [ev-30d6443900eb](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L71-L150) · 全文检索命中 pom.xml 第 71 至 150 行 · 读取时间 `2026-11-12T15:48:12.394333+00:00`
- [ev-347ae4770196](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:04:08.351027+00:00`
- [ev-4d6527e20885](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L71-L150) · 全文检索命中 langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 71 至 150 行 · 读取时间 `2026-11-12T15:50:59.131625+00:00`
- [ev-742942de347b](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) · 目录 /，文件名匹配 *bench*，展示偏移 0 后最多200项 · 读取时间 `2026-11-12T16:04:13.871112+00:00`
- [ev-7ef0d238786f](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) · 全文检索命中 langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 1 至 80 行 · 读取时间 `2026-11-12T15:50:59.131625+00:00`
- [ev-82bceb1d4b2b](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L80) · README.md 第 1 至 80 行，共 85 行 · 读取时间 `2026-11-12T16:04:13.663383+00:00` · 内容已截断
- [ev-9a359596b22c](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) · 目录 /，文件名匹配 *perf*，展示偏移 0 后最多200项 · 读取时间 `2026-11-12T16:04:15.239384+00:00`
- [ev-d0515d811308](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:04:09.599095+00:00`
- [ev-d580cf7d3a37](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L141-L193) · 全文检索命中 langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 141 至 193 行 · 读取时间 `2026-11-12T15:50:59.131625+00:00`
- [ev-ffe207e1f8a6](https://github.com/search?q=java+agent+framework+language%3Ajava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 4 个公开候选 · 读取时间 `2026-11-12T16:04:06.185638+00:00`

## 执行统计

```json
{
  "model_calls": 16,
  "input_tokens": 158987,
  "output_tokens": 5933,
  "estimated_cost_cny_upper_bound": 0.49542,
  "global_reserved_and_spent_cny": 13.926723,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": true,
  "run_unconfirmed_calls": 0,
  "github_requests": 7,
  "elapsed_seconds": 48.938,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 14,
      "cost_cny": 0.325176,
      "input_tokens": 143716,
      "output_tokens": 4718
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 2,
      "cost_cny": 0.170244,
      "input_tokens": 15271,
      "output_tokens": 1215
    }
  ],
  "retrieval": {
    "queries": 4,
    "returned_bytes": 12847,
    "seconds": 0.035937
  }
}
```

## 异常记录

- `invalid_query` 检索词长度应为 1 至 256，返回条数应为 1 至 5
- `invalid_query` 检索词长度应为 1 至 256，返回条数应为 1 至 5
- `retrieval` {"repository": "langchain4j/langchain4j", "query": "benchmark", "hits": 0, "bytes": 0}
- `retrieval` {"repository": "langchain4j/langchain4j", "query": "QPS", "hits": 0, "bytes": 0}
- `retrieval` {"repository": "langchain4j/langchain4j", "query": "throughput", "hits": 0, "bytes": 0}
- `retrieval` {"repository": "langchain4j/langchain4j", "query": "performance", "hits": 0, "bytes": 0}
- `retrieval` {"repository": "langchain4j/langchain4j", "query": "Agent", "hits": 4, "bytes": 12847}
- `validation_error` 候选必须经过 inspect_repository
- `analysis_limit` 深入分析的仓库数量达到上限
- `analysis_limit` 深入分析的仓库数量达到上限
- `analysis_limit` 深入分析的仓库数量达到上限
