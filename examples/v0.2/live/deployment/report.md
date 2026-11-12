# RepoScout 调研报告

搜索可用于 Java 后端的 Agent 项目，重点调研 alibaba/spring-ai-alibaba 的使用与部署资料，区分文档和实测。

任务 `d4cfde0aaf22` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T16:23:41.014622+00:00` · 维护判断窗口 180 天

## 需求与条件

调研可用于 Java 后端的 Agent 项目，重点分析 alibaba/spring-ai-alibaba 的使用与部署资料，并区分文档声明与实测结果。

- 可用于 Java 后端（硬性条件）
- 具备 Agent 能力（硬性条件）
- 提供使用与部署资料（偏好）

## alibaba/spring-ai-alibaba

面向 Java 开发者的 Agentic AI 框架，包含 Agent Framework、Graph 运行时、Admin 平台与 Spring Boot Starters；README 给出 JDK 17+ 前置条件、Maven 依赖坐标与 ChatBot 启动命令，examples 目录含可运行的配置样例。

固定 commit `17e26ff6fe951d605771c1845229ca3edb043634`

- **可用于 Java 后端 · 满足**。仓库语言为 Java，README 要求 JDK 17+，依赖坐标为 com.alibaba.cloud.ai 的 Maven 构件，示例通过 spring-boot:run 启动。 [ev-166e4c71cd94](https://github.com/alibaba/spring-ai-alibaba) [ev-7b16e513218a](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- **具备 Agent 能力 · 满足**。README 描述 Agent Framework 内置 SequentialAgent/ParallelAgent/RoutingAgent/LoopAgent 等编排模式，Graph 提供持久化与流式运行时。 [ev-7b16e513218a](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- **提供使用与部署资料 · 满足**。README 提供快速开始步骤、依赖片段与官方文档链接；examples/documentation 的 application.yml 展示 DashScope、A2A Nacos、MCP 客户端等配置项。 [ev-7b16e513218a](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140) [ev-2f1773ba4f3f](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59)

**推荐**。Java 语言、Agent 编排能力与文档/示例配置齐备，维护活跃（最近提交在 180 天窗口内），适合作为 Java 后端 Agent 选型首选；实际运行效果未实测。 [ev-166e4c71cd94](https://github.com/alibaba/spring-ai-alibaba) [ev-7b16e513218a](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140) [ev-2f1773ba4f3f](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59) [ev-afcb7d65f33e](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634)

- README 声明需 JDK 17+，ChatBot 示例通过 ./mvnw -pl examples/chatbot spring-boot:run 启动并访问 localhost:8080/chatui。（依据 `documentation`） [ev-7b16e513218a](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- 示例配置 application.yml 使用 DASHSCOPE_API_KEY 与 qwen-plus 模型，并配置 A2A Nacos 注册发现（需 Nacos 3.x+）及 MCP streamable-http/SSE 连接。（依据 `source`） [ev-2f1773ba4f3f](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59)
- 元数据：Apache-2.0 许可，约 1.1 万 stars，最近提交 2026-10-07，最新正式版 v1.1.2.2（2026-03-10），另有预发布 v2.0.0-M1.1。（依据 `metadata`） [ev-166e4c71cd94](https://github.com/alibaba/spring-ai-alibaba) [ev-afcb7d65f33e](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634)
- 未确认项 — 未实际运行示例，启动成功率、性能与资源占用未实测
- 未确认项 — Admin 平台与 Studio 的部署方式未读取源码验证
- 未确认项 — v2.0.0-M1.1 为预发布版本，稳定性未确认

## 结论

在已核验范围内，alibaba/spring-ai-alibaba 是唯一取得文件原文证据的候选：Java 语言、JDK 17+、Maven 依赖与 spring-boot:run 启动步骤、DashScope/A2A Nacos/MCP 配置样例齐备，维护活跃，推荐作为 Java 后端 Agent 选型首选。搜索另见 langchain4j/langchain4j、agents-flex/agents-flex、mateaix/mateclaw 等候选，但受分析额度限制未深入核验，结论待确认。所有运行效果、性能与部署实测均未进行，README 与配置中的能力属文档/源码声明。

## 未确认项

- 未实际运行任何候选项目，启动成功率、性能、资源占用均未实测
- Admin/Studio 平台部署方式未验证
- langchain4j、agents-flex、mateclaw 未做仓库内证据核验

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 1 轮 · 补证 0 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-166e4c71cd94](https://github.com/alibaba/spring-ai-alibaba) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:02:15.800523+00:00`
- [ev-2f1773ba4f3f](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59) · examples/documentation/src/main/resources/application.yml 第 1 至 59 行，共 59 行 · 读取时间 `2026-11-12T16:02:23.889541+00:00`
- [ev-450581d9ab49](https://github.com/search?q=java+agent+framework+language%3Ajava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 4 个公开候选 · 读取时间 `2026-11-12T16:02:13.039304+00:00`
- [ev-7b16e513218a](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140) · README.md 第 1 至 140 行，共 168 行 · 读取时间 `2026-11-12T16:02:23.742768+00:00` · 内容已截断
- [ev-878da604d49c](https://github.com/alibaba/spring-ai-alibaba/tree/17e26ff6fe951d605771c1845229ca3edb043634) · 最多展示前 300 个目录项 · 读取时间 `2026-11-12T16:02:19.408147+00:00` · 内容已截断
- [ev-afcb7d65f33e](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:02:17.311695+00:00`
- [ev-fc32c0453139](https://github.com/search?q=spring-ai-alibaba&type=repositories) · GitHub 搜索，返回 10 个公开候选 · 读取时间 `2026-11-12T16:02:13.301059+00:00`

## 执行统计

```json
{
  "model_calls": 13,
  "input_tokens": 136558,
  "output_tokens": 5809,
  "estimated_cost_cny_upper_bound": 0.431502,
  "global_reserved_and_spent_cny": 13.926723,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": true,
  "run_unconfirmed_calls": 0,
  "github_requests": 9,
  "elapsed_seconds": 46.842,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 11,
      "cost_cny": 0.284442,
      "input_tokens": 123917,
      "output_tokens": 4576
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 2,
      "cost_cny": 0.14706,
      "input_tokens": 12641,
      "output_tokens": 1233
    }
  ],
  "retrieval": {}
}
```

## 异常记录

- `analysis_limit` 深入分析的仓库数量达到上限
- `analysis_limit` 深入分析的仓库数量达到上限
- `validation_error` 候选必须经过 inspect_repository
