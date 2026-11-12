# RepoScout 调研报告

搜索 Java Agent 框架，比较 langchain4j/langchain4j 与 alibaba/spring-ai-alibaba 的技术栈与使用方式，给出来源。

任务 `a88faa5403b4` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T16:23:41.019981+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 框架，重点比较 langchain4j/langchain4j 与 alibaba/spring-ai-alibaba 的技术栈与使用方式，并给出来源证据。

- Java Agent 框架（硬性条件）
- 技术栈（偏好）
- 使用方式（偏好）

## langchain4j/langchain4j

面向 JVM 的惯用 Java LLM 库，提供统一模型/向量库 API，工具箱覆盖 prompt 模板、chat memory、function calling 到 Agents 与 RAG；agentic 模块以 @Agent 注解声明式定义 agent。

固定 commit `b7fe277c7437145617bcd49b77febfa5698c9ef4`

- **Java Agent 框架 · 满足**。README 将 Agents 列为工具箱中的高层模式，且存在 langchain4j-agentic 模块的 @Agent 注解源码。 [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85) [ev-09465efc6ec0](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80)
- **技术栈 · 满足**。Java 库，Maven 发布（dev.langchain4j），可独立使用或集成 Quarkus/Spring Boot/Helidon/Micronaut。 [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85) [ev-40834a5858e0](https://github.com/langchain4j/langchain4j)
- **使用方式 · 满足**。以 Java 注解/接口声明 agent（@Agent 标注方法），并提供 plain Java、Quarkus、Spring Boot 等示例入口。 [ev-09465efc6ec0](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85)

**推荐**。满足 Java Agent 框架定位，技术栈为纯 Java 库、框架无关，使用方式为注解式声明 agent；维护活跃（当日提交、近期发布）。 [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85) [ev-09465efc6ec0](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) [ev-40834a5858e0](https://github.com/langchain4j/langchain4j) [ev-24d3cfe35c44](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)

- README 声明其目标是简化 LLM 集成，提供统一 API，支持 20+ LLM 提供商与 30+ embedding store。（依据 `documentation`） [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85)
- README 明确 LangChain4j 不是 Python LangChain 的移植，而是围绕 Java 惯例（类型安全、POJO、注解、接口、DI、流式 API）从零设计，并与 Quarkus、Spring Boot、Helidon、Micronaut 集成。（依据 `documentation`） [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85)
- 源码中 @Agent 是标注在 Java 方法上的运行时注解，方法即 agent，可被其他 agent 调用，支持 name/description/outputKey/typedOutputKey 等属性。（依据 `source`） [ev-09465efc6ec0](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80)
- 元数据：Apache-2.0，约 13.4k stars，最近提交 2026-11-12，最近发布 1.19.5（2026-11-02）。（依据 `metadata`） [ev-40834a5858e0](https://github.com/langchain4j/langchain4j) [ev-24d3cfe35c44](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4)
- 未确认项 — 未实测 agent 编排性能与运行时行为
- 未确认项 — 未读取 pom.xml 确认最低 JDK 版本

## alibaba/spring-ai-alibaba

基于 Spring AI 的 Agentic AI 框架，由 Agent Framework、Graph 运行时与 Admin 平台组成，内置多智能体编排模式、上下文工程、A2A 与 MCP 支持，通过 Spring Boot starter 与 YAML 配置使用。

固定 commit `17e26ff6fe951d605771c1845229ca3edb043634`

- **Java Agent 框架 · 满足**。README 明确为 Agentic AI 框架，含 Agent Framework 与多智能体编排模式。 [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- **技术栈 · 满足**。Java + Spring Boot + Spring AI 生态，依赖 Maven 坐标 com.alibaba.cloud.ai，要求 JDK 17+。 [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- **使用方式 · 满足**。以 Spring Boot starter 依赖 + application.yml 配置（模型、MCP、A2A/Nacos）方式使用，另有 Admin 可视化平台。 [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140) [ev-4580b0b5e647](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59)

**推荐**。满足 Java Agent 框架定位，技术栈绑定 Spring AI/Spring Boot，使用方式为 starter + YAML 配置；维护窗口内仍有提交，但最近一次提交距今天约 36 天，最新发布为预发布版。 [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140) [ev-4580b0b5e647](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59) [ev-c6479813222f](https://github.com/alibaba/spring-ai-alibaba) [ev-67f10d2c9fc3](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634)

- README 定位为构建 Agentic、Workflow 与多智能体应用的生产级框架，内置 SequentialAgent/ParallelAgent/RoutingAgent/LoopAgent 等编排模式。（依据 `documentation`） [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- README 说明 Graph 是 Agent Framework 的底层运行时，提供持久化、工作流编排与流式能力；项目含 agent-framework、graph、admin、studio、spring-boot-starters 模块。（依据 `documentation`） [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- 使用方式为 Spring Boot：引入 spring-ai-alibaba-agent-framework 与 spring-ai-alibaba-starter-dashscope 依赖，要求 JDK 17+，示例通过 ./mvnw -pl examples/chatbot spring-boot:run 启动。（依据 `documentation`） [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140)
- 示例 application.yml 通过 spring.ai.dashscope 配置 api-key 与 qwen-plus 模型，并配置 spring.ai.mcp.client（streamable-http/sse）及 spring.ai.alibaba.a2a.nacos 服务发现与注册。（依据 `source`） [ev-4580b0b5e647](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59)
- 元数据：Apache-2.0，约 11.1k stars，最近提交 2026-10-07，最近发布为预发布 v2.0.0-M1.1（2026-06-25），稳定版 v1.1.2.2（2026-03-10）。（依据 `metadata`） [ev-c6479813222f](https://github.com/alibaba/spring-ai-alibaba) [ev-67f10d2c9fc3](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634)
- 未确认项 — 未实测 Graph 运行时与多智能体编排性能
- 未确认项 — 未读取 pom.xml 确认具体 Spring AI 版本依赖
- 未确认项 — Admin 平台独立部署效果未验证

## 结论

两者均为 Java Agent 框架且维护在窗口内。langchain4j 是框架无关的纯 Java 库，以 @Agent 注解/接口声明 agent，可独立或嵌入 Quarkus/Spring Boot 等；spring-ai-alibaba 深度绑定 Spring AI/Spring Boot，以 starter 依赖 + YAML 配置驱动，并提供 Graph 运行时、多智能体编排模式、A2A/MCP 与 Admin 可视化平台。若项目已在 Spring Boot 且需要图编排与平台化能力，后者更贴合；若需轻量、框架无关的 Java 库，前者更合适。性能与运行效果均未实测。

## 未确认项

- 未运行任何示例，性能与稳定性未实测
- 未核对两仓库最低 JDK 与依赖版本矩阵的完整细节

## 模型辅助核验

状态 `passed` · 模型 `deepseek-v4-pro` · 核验 1 轮 · 补证 0 轮

模型辅助审查，事实语义需结合引用原文复核


## 证据索引

- [ev-0680a6ede790](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/README.md#L1-L85) · README.md 第 1 至 85 行，共 85 行 · 读取时间 `2026-11-12T16:03:13.852580+00:00`
- [ev-09465efc6ec0](https://github.com/langchain4j/langchain4j/blob/b7fe277c7437145617bcd49b77febfa5698c9ef4/langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java#L1-L80) · langchain4j-agentic/src/main/java/dev/langchain4j/agentic/Agent.java 第 1 至 80 行，共 193 行 · 读取时间 `2026-11-12T16:03:13.236535+00:00` · 内容已截断
- [ev-24d3cfe35c44](https://github.com/langchain4j/langchain4j/commits/b7fe277c7437145617bcd49b77febfa5698c9ef4) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:03:10.699305+00:00`
- [ev-356077d32795](https://github.com/search?q=java+agent+framework+language%3AJava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 4 个公开候选 · 读取时间 `2026-11-12T16:03:07.467184+00:00`
- [ev-40834a5858e0](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:03:09.551176+00:00`
- [ev-4580b0b5e647](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/examples/documentation/src/main/resources/application.yml#L1-L59) · examples/documentation/src/main/resources/application.yml 第 1 至 59 行，共 59 行 · 读取时间 `2026-11-12T16:03:13.416375+00:00`
- [ev-67f10d2c9fc3](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T16:03:09.458341+00:00`
- [ev-c6479813222f](https://github.com/alibaba/spring-ai-alibaba) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T16:03:08.227363+00:00`
- [ev-eee1a793e6be](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L140) · README.md 第 1 至 140 行，共 168 行 · 读取时间 `2026-11-12T16:03:13.243525+00:00` · 内容已截断

## 执行统计

```json
{
  "model_calls": 8,
  "input_tokens": 80333,
  "output_tokens": 5917,
  "estimated_cost_cny_upper_bound": 0.445164,
  "global_reserved_and_spent_cny": 13.926723,
  "unconfirmed_calls": 1,
  "billing_blocked": false,
  "usage_complete": true,
  "run_unconfirmed_calls": 0,
  "github_requests": 13,
  "elapsed_seconds": 48.972,
  "models": [
    {
      "model": "deepseek-flash",
      "role": "research",
      "calls": 5,
      "cost_cny": 0.134052,
      "input_tokens": 52986,
      "output_tokens": 3510
    },
    {
      "model": "deepseek-v4-pro",
      "role": "review",
      "calls": 3,
      "cost_cny": 0.311112,
      "input_tokens": 27347,
      "output_tokens": 2407
    }
  ],
  "retrieval": {}
}
```
