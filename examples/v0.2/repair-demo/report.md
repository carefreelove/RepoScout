# RepoScout 调研报告

确认 langchain4j/langchain4j 的 Java 构建目标。请使用全文检索工具检索 java.version，补齐源码依据，再修正草稿并提交。

任务 `227e4890ac02` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T16:08:25.775804+00:00` · 维护判断窗口 180 天

## 需求与条件

确认 langchain4j/langchain4j 的 Java 构建目标，并以全文检索 java.version 得到的源码依据修正草稿后提交。

- 确认 Java 构建目标（硬性条件）

## langchain4j/langchain4j

LangChain4j 是面向 JVM 的 Java LLM 应用库（Apache-2.0）。其父 POM 将 java.version 设为 17，并以此驱动 maven.compiler.release 与 Kotlin jvmTarget，即构建目标为 Java 17。

固定 commit `b7fe277c7437145617bcd49b77febfa5698c9ef4`

- **确认 Java 构建目标 · 满足**。langchain4j-parent/pom.xml 第 39 行明确 <java.version>17</java.version>，且第 40、42 行将其用于 maven.compiler.release 与 Kotlin jvmTarget，构建目标为 Java 17。 [ev-1f12d3dd4de5](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-parent/pom.xml#L1-L120)

**推荐**。构建目标已由父 POM 源码明确为 Java 17，并有编译 release 与 Kotlin jvmTarget 的联动配置佐证；仓库维护活跃。 [ev-1f12d3dd4de5](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-parent/pom.xml#L1-L120) [ev-3a8e0f5d1976](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L141-L220) [ev-ff393c600b77](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L211-L290) [ev-cc531204cd1e](https://github.com/langchain4j/langchain4j) [ev-eee0469cd401](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)

- langchain4j-parent/pom.xml 第 39 行定义 <java.version>17</java.version>。（依据 `source`） [ev-1f12d3dd4de5](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-parent/pom.xml#L1-L120)
- 第 40 行 <maven.compiler.release>${java.version}</maven.compiler.release>，编译 release 目标继承 17。（依据 `source`） [ev-1f12d3dd4de5](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-parent/pom.xml#L1-L120)
- 第 42 行 kotlin.compiler.jvmTarget 同样引用 ${java.version}，Kotlin 模块目标一致为 17。（依据 `source`） [ev-1f12d3dd4de5](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-parent/pom.xml#L1-L120)
- 根聚合 pom.xml 的 properties 段（第 156-160 行）未定义 java.version，构建目标由 langchain4j-parent 统一管理。（依据 `source`） [ev-3a8e0f5d1976](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L141-L220)
- 根 pom 定义 jdk21 与 jdk25 激活 profile，仅用于追加 langchain4j-jlama、langchain4j-jitllm、langchain4j-gpu-llama3 等模块，不改变基础构建目标。（依据 `source`） [ev-ff393c600b77](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L211-L290)
- 仓库近期活跃：最新提交 2026-11-12，最近发布 1.19.5（2026-11-02），Apache-2.0 许可，约 1.34 万 stars。（依据 `metadata`） [ev-cc531204cd1e](https://github.com/langchain4j/langchain4j) [ev-eee0469cd401](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- 未确认项 — 未运行构建，未实测在 JDK 17 及以上各版本的实际编译/运行表现
- 未确认项 — 各子模块是否单独覆盖 java.version 未逐一核查

## 结论

langchain4j/langchain4j 的 Java 构建目标为 17：父 POM 定义 java.version=17，并作为 maven.compiler.release 与 Kotlin jvmTarget 的取值；根 POM 的 jdk21/jdk25 profile 仅按 JDK 版本追加可选模块，不改变基础目标。

## 未确认项

- 未实测构建与运行效果
- 子模块级覆盖情况未逐一核查

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 2 轮 · 补证 1 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-018699abed9f](https://github.com/langchain4j/langchain4j/tree/b7fe277c7437145617bcd49b77febfa5698c9ef4/) · 目录 /，文件名匹配 pom.xml，展示偏移 0 后最多200项 · 读取时间 `2026-11-12T16:08:06.551485+00:00`
- [ev-1f12d3dd4de5](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-parent/pom.xml#L1-L120) · langchain4j-parent/pom.xml 第 1 至 120 行，共 1090 行 · 读取时间 `2026-11-12T16:08:08.442057+00:00` · 内容已截断
- [ev-3a8e0f5d1976](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L141-L220) · 全文检索命中 pom.xml 第 141 至 220 行 · 读取时间 `2026-11-12T15:48:12.394333+00:00` · 内容已截断
- [ev-576c914ee846](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L281-L321) · 全文检索命中 pom.xml 第 281 至 321 行 · 读取时间 `2026-11-12T15:48:12.394333+00:00` · 内容已截断
- [ev-58122da7b2eb](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85) · README.md 第 1 至 85 行，共 85 行 · 读取时间 `2026-11-12T16:07:58.434504+00:00`
- [ev-641b5442619c](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L1-L80) · 全文检索命中 pom.xml 第 1 至 80 行 · 读取时间 `2026-11-12T15:48:12.394333+00:00` · 内容已截断
- [ev-cc531204cd1e](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:07:55.866422+00:00`
- [ev-eee0469cd401](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:07:57.890950+00:00`
- [ev-ff393c600b77](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/pom.xml#L211-L290) · 全文检索命中 pom.xml 第 211 至 290 行 · 读取时间 `2026-11-12T15:48:12.394333+00:00` · 内容已截断

## 执行统计

```json
{
  "model_calls": 8,
  "input_tokens": 80970,
  "output_tokens": 3360,
  "estimated_cost_cny_upper_bound": 0.339831,
  "global_reserved_and_spent_cny": 13.868277,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": true,
  "run_unconfirmed_calls": 0,
  "github_requests": 7,
  "elapsed_seconds": 31.471,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 5,
      "cost_cny": 0.141714,
      "input_tokens": 63577,
      "output_tokens": 1820
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 3,
      "cost_cny": 0.198117,
      "input_tokens": 17393,
      "output_tokens": 1540
    }
  ],
  "retrieval": {
    "queries": 1,
    "returned_bytes": 12689,
    "seconds": 0.012281
  }
}
```

## 异常记录

- `review_issues` 第 1 轮发现 5 项待处理问题
- `invalid_query` 检索词长度应为 1 至 256，返回条数应为 1 至 5
- `retrieval` {"repository": "langchain4j/langchain4j", "query": "java.version", "hits": 4, "bytes": 12689}
