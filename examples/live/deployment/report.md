# RepoScout 调研报告

搜索可用于 Java 后端的 Agent 项目，重点调研 alibaba/spring-ai-alibaba 的使用与部署资料，区分文档和实测。

任务 `a712e7066ce1` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T10:11:21.977372+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索可用于 Java 后端的 Agent 项目，重点调研 alibaba/spring-ai-alibaba 的使用与部署资料，并区分文档声明与实测证据。

- 可用于 Java 后端（硬性条件）
- Agent 项目（硬性条件）
- 提供使用与部署资料（偏好）

## alibaba/spring-ai-alibaba

Java 语言的 Agentic AI 框架，含 Agent Framework、Graph 运行时、Admin 平台与 Spring Boot starters；README 提供 JDK 17+ 前置条件、ChatBot 快速启动命令与依赖坐标。

固定 commit `17e26ff6fe951d605771c1845229ca3edb043634`

- **可用于 Java 后端 · 满足**。仓库语言为 Java，示例 pom 以 spring-boot-starter-parent 3.5.7 为父工程并设置 java.version=17，依赖 Spring Boot Web 与 Spring AI 组件。 [ev-284520d7a9ad](https://github.com/alibaba/spring-ai-alibaba) [ev-35970f38b364](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/pom.xml#L1-L120)
- **Agent 项目 · 满足**。README 自述为构建 Agentic、Workflow 与多 Agent 应用的生产级框架，并列出 SequentialAgent/ParallelAgent/RoutingAgent/LoopAgent 等编排模式。 [ev-55c5be9ab08b](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- **提供使用与部署资料 · 满足**。README 给出 JDK 17+ 前置条件、设置 AI_DASHSCOPE_API_KEY、./mvnw -pl examples/chatbot spring-boot:run 启动命令及 Maven 依赖坐标；examples/chatbot/README 重复同样步骤。 [ev-55c5be9ab08b](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120) [ev-9495fa0df738](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/chatbot/README.md#L1-L40)

**推荐**。三项条件均有文档或源码证据支持；维护窗口 180 天内（截至 2026-11-12）有提交与预发布版本，正式版为 2026-03 的 v1.1.2.2。 [ev-55c5be9ab08b](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120) [ev-35970f38b364](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/pom.xml#L1-L120) [ev-284520d7a9ad](https://github.com/alibaba/spring-ai-alibaba) [ev-a7eb68d20454](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634) [ev-9495fa0df738](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/chatbot/README.md#L1-L40)

- README 声明为生产级 Agentic/Workflow/多 Agent 框架，含 Agent Framework、Graph 运行时与 Admin 一站式平台。（依据 `documentation`） [ev-55c5be9ab08b](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- 示例 pom 使用 Spring Boot 3.5.7 父工程、java.version=17、spring-ai 1.1.2 与 spring-ai-alibaba 1.1.2.2，并引入 agent-framework、dashscope starter、studio、a2a-nacos 等依赖。（依据 `source`） [ev-35970f38b364](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/pom.xml#L1-L120)
- 元数据：Apache-2.0，Java，约 1.11 万 stars，最近推送 2026-10-07，最新正式版 v1.1.2.2（2026-03-10），另有预发布 v2.0.0-M1.1（2026-06-25）。（依据 `metadata`） [ev-284520d7a9ad](https://github.com/alibaba/spring-ai-alibaba) [ev-a7eb68d20454](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634)
- 未确认项 — 未实际运行示例，启动命令与 ChatBot 界面可用性属文档声明，无实测
- 未确认项 — 生产部署（Admin 平台、集群、持久化存储）的部署文档与运行效果未验证
- 未确认项 — 性能与并发基准无证据

## 结论

alibaba/spring-ai-alibaba 是面向 Java 后端的 Agent 框架，使用与部署资料以 README 与 examples/chatbot 文档为主（JDK 17+、DashScope API Key、mvnw 启动），源码层面确认 Spring Boot 3.5.7 + Java 17 + spring-ai-alibaba 1.1.2.2 依赖组合。所有运行效果均为文档声明，未做实测；搜索到的其他候选未深入分析。

## 未确认项

- 未对搜索返回的其他候选仓库做深入分析
- 未实测任何仓库的启动、部署与性能表现

## 证据索引

- [ev-01fd3378e91b](https://github.com/search?q=spring-ai-alibaba&type=repositories) · GitHub 搜索，返回 10 个公开候选 · 读取时间 `2026-11-12T10:10:51.708802+00:00`
- [ev-284520d7a9ad](https://github.com/alibaba/spring-ai-alibaba) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T10:10:54.315527+00:00`
- [ev-35970f38b364](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/pom.xml#L1-L120) · examples/documentation/pom.xml 第 1 至 120 行，共 200 行 · 读取时间 `2026-11-12T10:11:12.441700+00:00` · 内容已截断
- [ev-55c5be9ab08b](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120) · README.md 第 1 至 120 行，共 168 行 · 读取时间 `2026-11-12T10:11:09.887256+00:00` · 内容已截断
- [ev-646e2f6b284d](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L120-L168) · README.md 第 120 至 168 行，共 168 行 · 读取时间 `2026-11-12T10:11:05.147120+00:00` · 内容已截断
- [ev-7328145ecf5f](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L120-L168) · README.md 第 120 至 168 行，共 168 行 · 读取时间 `2026-11-12T10:11:12.441327+00:00` · 内容已截断
- [ev-82f192dd24c5](https://github.com/alibaba/spring-ai-alibaba/tree/17e26ff6fe951d605771c1845229ca3edb043634) · 最多展示前 300 个目录项 · 读取时间 `2026-11-12T10:11:05.154604+00:00` · 内容已截断
- [ev-9495fa0df738](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/chatbot/README.md#L1-L40) · examples/chatbot/README.md 第 1 至 40 行，共 40 行 · 读取时间 `2026-11-12T10:11:10.491379+00:00`
- [ev-a7eb68d20454](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T10:10:55.321281+00:00`
- [ev-b70c05f3df18](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120) · README.md 第 1 至 120 行，共 168 行 · 读取时间 `2026-11-12T10:11:03.197337+00:00` · 内容已截断
- [ev-d796f1212184](https://github.com/alibaba/spring-ai-alibaba/tree/17e26ff6fe951d605771c1845229ca3edb043634) · 最多展示前 300 个目录项 · 读取时间 `2026-11-12T10:10:57.465494+00:00` · 内容已截断
- [ev-e03aa98529df](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/pom.xml#L1-L120) · examples/documentation/pom.xml 第 1 至 120 行，共 200 行 · 读取时间 `2026-11-12T10:11:03.401352+00:00` · 内容已截断
- [ev-f908fea983b4](https://github.com/search?q=java+agent+framework+language%3Ajava+stars%3A%3E500&type=repositories) · GitHub 搜索，返回 4 个公开候选 · 读取时间 `2026-11-12T10:10:51.553654+00:00`

## 执行统计

```json
{
  "model_calls": 13,
  "input_tokens": 131138,
  "output_tokens": 3417,
  "estimated_cost_cny_upper_bound": 0.289612,
  "global_reserved_and_spent_cny": 9.511242,
  "unconfirmed_calls": 0,
  "github_requests": 10,
  "elapsed_seconds": 34.345
}
```
