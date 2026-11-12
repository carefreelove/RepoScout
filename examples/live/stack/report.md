# RepoScout 调研报告

搜索支持 Java 的开源 LLM Agent 框架，重点调研 langchain4j/langchain4j，给出依赖或源码依据。

任务 `a0127c7f112a` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T10:10:09.970996+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索支持 Java 的开源 LLM Agent 框架，重点调研 langchain4j/langchain4j，并给出依赖或源码依据。

- 开源（硬性条件）
- 支持 Java（硬性条件）
- 提供 LLM Agent 框架能力（硬性条件）

## langchain4j/langchain4j

LangChain4j 是面向 JVM 的 Java LLM 应用库，提供统一 LLM/向量库 API、工具调用、Agent 与 RAG 能力，并含独立的 langchain4j-agentic 模块。

固定 commit `fb6e252b7a67e0d0579957127cafea9202ba1019`

- **开源 · 满足**。父 POM 声明 Apache-2.0 许可证，元数据 license 为 Apache-2.0，仓库未归档。 [ev-0fc601b726be](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-parent/pom.xml#L1-L60) [ev-d7c87b468e9b](https://github.com/langchain4j/langchain4j)
- **支持 Java · 满足**。元数据语言为 Java；父 POM 设置 java.version=17 与 maven.compiler.release，核心模块 langchain4j 为 Maven 构件。 [ev-d7c87b468e9b](https://github.com/langchain4j/langchain4j) [ev-0fc601b726be](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-parent/pom.xml#L1-L60) [ev-08e28ea40660](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j/pom.xml#L1-L80)
- **提供 LLM Agent 框架能力 · 满足**。README 列出 Agents 高层模式；仓库含 langchain4j-agentic 模块（Agentic Framework），依赖核心 langchain4j。 [ev-d9fe9054c5ae](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85) [ev-491dd5ad0f7a](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-agentic/pom.xml#L1-L60)

**推荐**。三项硬性条件均有依赖/源码或文档证据支持，且维护活跃（近期提交与发布均在 180 天窗口内）。 [ev-d9fe9054c5ae](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85) [ev-0fc601b726be](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-parent/pom.xml#L1-L60) [ev-491dd5ad0f7a](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-agentic/pom.xml#L1-L60) [ev-d7c87b468e9b](https://github.com/langchain4j/langchain4j) [ev-399964490e05](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)

- README 自述为开源、惯用 Java 的 LLM 应用库，工具箱覆盖 prompt 模板、chat memory、function calling 到 Agents 与 RAG 等高层模式。（依据 `documentation`） [ev-d9fe9054c5ae](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)
- 父 POM 声明 Apache-2.0 许可证，java.version=17 并作为 maven.compiler.release，说明构建目标为 Java 17。（依据 `source`） [ev-0fc601b726be](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-parent/pom.xml#L1-L60)
- langchain4j-agentic/pom.xml 定义 artifactId 为 langchain4j-agentic、name 为 Agentic Framework，依赖 dev.langchain4j:langchain4j。（依据 `source`） [ev-491dd5ad0f7a](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-agentic/pom.xml#L1-L60)
- 仓库元数据：语言 Java，Apache-2.0，未归档，约 13.4k stars；最近提交 2026-11-12，最近发布 1.19.5（2026-11-02）。（依据 `metadata`） [ev-d7c87b468e9b](https://github.com/langchain4j/langchain4j) [ev-399964490e05](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)
- 未确认项 — 未运行目标代码，Agent 编排的实际性能与稳定性缺乏实测
- 未确认项 — langchain4j-agentic 模块的 API 细节未逐文件阅读

## 结论

langchain4j/langchain4j 满足开源、Java、LLM Agent 框架三项条件，可作为首选候选；其 Agent 能力由核心库 Agents 模式与 langchain4j-agentic 模块共同提供，构建基线为 Java 17。搜索到的其他候选未深入分析，不构成排除结论。

## 未确认项

- 其他搜索结果候选未做证据级分析
- 未进行基准测试，性能与部署效果未确认

## 证据索引

- [ev-08e28ea40660](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j/pom.xml#L1-L80) · langchain4j/pom.xml 第 1 至 80 行，共 227 行 · 读取时间 `2026-11-12T10:10:01.874391+00:00` · 内容已截断
- [ev-0fc601b726be](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-parent/pom.xml#L1-L60) · langchain4j-parent/pom.xml 第 1 至 60 行，共 1090 行 · 读取时间 `2026-11-12T10:10:00.385237+00:00` · 内容已截断
- [ev-399964490e05](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T10:09:50.986901+00:00`
- [ev-491dd5ad0f7a](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j-agentic/pom.xml#L1-L60) · langchain4j-agentic/pom.xml 第 1 至 60 行，共 169 行 · 读取时间 `2026-11-12T10:10:00.269304+00:00` · 内容已截断
- [ev-4b227ac6966b](https://github.com/search?q=java+llm+agent+framework+language%3AJava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 2 个公开候选 · 读取时间 `2026-11-12T10:09:48.049038+00:00`
- [ev-974cbc59fb0a](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L121-L200) · pom.xml 第 121 至 200 行，共 321 行 · 读取时间 `2026-11-12T10:09:57.892852+00:00` · 内容已截断
- [ev-9b183c60fc25](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/pom.xml#L1-L120) · pom.xml 第 1 至 120 行，共 321 行 · 读取时间 `2026-11-12T10:09:54.875106+00:00` · 内容已截断
- [ev-d7c87b468e9b](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T10:09:49.904105+00:00`
- [ev-d9fe9054c5ae](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85) · README.md 第 1 至 85 行，共 85 行 · 读取时间 `2026-11-12T10:10:01.874059+00:00`
- [ev-ec92a19223d8](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/langchain4j/pom.xml#L1-L80) · langchain4j/pom.xml 第 1 至 80 行，共 227 行 · 读取时间 `2026-11-12T10:09:56.617612+00:00` · 内容已截断
- [ev-f00318adf3f1](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85) · README.md 第 1 至 85 行，共 85 行 · 读取时间 `2026-11-12T10:09:54.869279+00:00`
- [ev-f0ab9fcfebcb](https://github.com/search?q=langchain4j+in%3Aname&type=repositories) · GitHub 搜索，返回 10 个公开候选 · 读取时间 `2026-11-12T10:09:48.217390+00:00`

## 执行统计

```json
{
  "model_calls": 12,
  "input_tokens": 124445,
  "output_tokens": 2491,
  "estimated_cost_cny_upper_bound": 0.268818,
  "global_reserved_and_spent_cny": 9.04153,
  "unconfirmed_calls": 0,
  "github_requests": 12,
  "elapsed_seconds": 25.678
}
```

## 异常记录

- `response_too_large` GitHub 响应超过 2 MB 限制
- `invalid_range` 每次最多读取 200 行，行号从 1 开始
