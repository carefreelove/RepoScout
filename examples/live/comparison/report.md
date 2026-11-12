# RepoScout 调研报告

搜索 Java Agent 框架，比较 langchain4j/langchain4j 与 alibaba/spring-ai-alibaba 的技术栈与使用方式，给出来源。

任务 `85408e0cc9b9` · 状态 `completed` · 模式 `live`

生成时间 `2026-11-12T10:12:00.170925+00:00` · 维护判断窗口 180 天

## 需求与条件

搜索 Java Agent 框架，比较 langchain4j/langchain4j 与 alibaba/spring-ai-alibaba 的技术栈与使用方式，并给出来源。

- Java Agent 框架（硬性条件）
- 技术栈（偏好）
- 使用方式（偏好）

## langchain4j/langchain4j

面向 JVM 的惯用 Java LLM 应用库，提供统一模型/向量库 API、工具箱（提示模板、记忆、函数调用、Agent、RAG）及多框架集成。

固定 commit `fb6e252b7a67e0d0579957127cafea9202ba1019`

- **Java Agent 框架 · 满足**。README 明确工具箱包含 Agents 与 RAG 等高层模式，并定位为 Java 库。 [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)
- **技术栈 · 满足**。统一 API 覆盖 20+ LLM 提供商与 30+ 向量库，基于 Java 类型安全、注解、接口、DI、流式 API。 [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)
- **使用方式 · 满足**。Maven 坐标 dev.langchain4j:langchain4j，提供纯 Java、Spring Boot、Quarkus、Helidon、Micronaut 示例。 [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)

**推荐**。README 证据显示其具备 Agent/RAG 能力、统一多模型 API 与多框架集成示例，符合 Java Agent 框架定位。 [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85) [ev-cae0ceb8ad6a](https://github.com/langchain4j/langchain4j) [ev-d4469d62c9a6](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019)

- 定位为 JVM 上构建 LLM 应用的惯用开源 Java 库，非 Python LangChain 的移植。（依据 `documentation`） [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)
- 统一 API 支持 20+ LLM 提供商与 30+ 向量存储，可切换而不改代码。（依据 `documentation`） [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)
- 工具箱含提示模板、聊天记忆、函数调用、Agent 与 RAG，并提供 Spring Boot/Quarkus/Helidon/Micronaut 示例。（依据 `documentation`） [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85)
- 未确认项 — 未实测性能与部署效果
- 未确认项 — 未读取依赖清单确认 JDK 版本要求

## alibaba/spring-ai-alibaba

基于 Spring AI 的生产级 Agent/工作流/多智能体框架，含 Agent Framework、Graph 运行时与 Admin 平台。

固定 commit `17e26ff6fe951d605771c1845229ca3edb043634`

- **Java Agent 框架 · 满足**。README 自述为构建 Agentic、Workflow、Multi-agent 应用的生产级框架，内置 SequentialAgent 等模式。 [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- **技术栈 · 满足**。基于 Spring AI 核心概念，JDK 17+，Maven 坐标 com.alibaba.cloud.ai，支持 DashScope/OpenAI 等模型与 MCP。 [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- **使用方式 · 满足**。引入 spring-ai-alibaba-agent-framework 与 starter-dashscope 依赖，设置 API-KEY 后 mvnw spring-boot:run 启动示例。 [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)

**推荐**。README 证据显示其提供 Agent Framework、Graph 工作流与 Spring Boot 快速启动方式，符合 Java Agent 框架定位。 [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120) [ev-1922c4aa1fe5](https://github.com/alibaba/spring-ai-alibaba) [ev-0dedd425883a](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634)

- 自述为生产级 Agentic/Workflow/Multi-agent 框架，含 Context Engineering 与 Human In The Loop。（依据 `documentation`） [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- Graph 作为底层运行时提供持久化、工作流编排与流式能力；另有 Admin 可视化平台。（依据 `documentation`） [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- 要求 JDK 17+，依赖 spring-ai-alibaba-agent-framework 1.1.2.0 与 starter-dashscope 1.1.2.1。（依据 `documentation`） [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120)
- 未确认项 — 未实测性能与部署效果
- 未确认项 — 未读取 pom 确认完整依赖树

## 结论

两者均为 Java Agent 框架。langchain4j 是框架无关的惯用 Java 库，统一 20+ 模型与 30+ 向量库 API，工具箱覆盖 Agent/RAG，可集成 Spring Boot、Quarkus、Helidon、Micronaut；spring-ai-alibaba 构建在 Spring AI 之上，强调 Agent Framework + Graph 工作流 + Admin 平台，需 JDK 17+ 并以 Spring Boot starter 方式使用。选型上：需要多框架、多模型统一抽象与 RAG 工具箱选 langchain4j；需要 Spring 生态、图工作流与多智能体编排选 spring-ai-alibaba。性能与部署效果均未实测。

## 未确认项

- 两仓库性能基准未实测
- 未读取依赖清单确认完整 JDK/Spring 版本约束

## 证据索引

- [ev-0dedd425883a](https://github.com/alibaba/spring-ai-alibaba/commits/17e26ff6fe951d605771c1845229ca3edb043634) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T10:11:36.697981+00:00`
- [ev-1922c4aa1fe5](https://github.com/alibaba/spring-ai-alibaba) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T10:11:35.052833+00:00`
- [ev-3bf7097d44ef](https://github.com/search?q=java+agent+framework+language%3AJava+stars%3A%3E1000&type=repositories) · GitHub 搜索，返回 4 个公开候选 · 读取时间 `2026-11-12T10:11:32.688930+00:00`
- [ev-4942bafd7041](https://github.com/langchain4j/langchain4j/blob/fb6e252b7a67e0d0579957127cafea9202ba1019/README.md#L1-L85) · README.md 第 1 至 85 行，共 85 行 · 读取时间 `2026-11-12T10:11:50.967553+00:00`
- [ev-764964acfc71](https://github.com/alibaba/spring-ai-alibaba/tree/17e26ff6fe951d605771c1845229ca3edb043634) · 最多展示前 300 个目录项 · 读取时间 `2026-11-12T10:11:45.290327+00:00` · 内容已截断
- [ev-cae0ceb8ad6a](https://github.com/langchain4j/langchain4j) · 仓库元数据快照，状态适用于读取时间 · 读取时间 `2026-11-12T10:11:35.111152+00:00`
- [ev-d4469d62c9a6](https://github.com/langchain4j/langchain4j/commits/fb6e252b7a67e0d0579957127cafea9202ba1019) · 近期提交及 release 快照，维护判断需结合时间窗口 · 读取时间 `2026-11-12T10:11:36.189937+00:00`
- [ev-f0b31894e061](https://github.com/alibaba/spring-ai-alibaba/blob/17e26ff6fe951d605771c1845229ca3edb043634/README.md#L1-L120) · README.md 第 1 至 120 行，共 168 行 · 读取时间 `2026-11-12T10:11:50.962127+00:00` · 内容已截断

## 执行统计

```json
{
  "model_calls": 7,
  "input_tokens": 62412,
  "output_tokens": 2880,
  "estimated_cost_cny_upper_bound": 0.147864,
  "global_reserved_and_spent_cny": 9.66908,
  "unconfirmed_calls": 0,
  "github_requests": 13,
  "elapsed_seconds": 30.226
}
```

## 异常记录

- `response_too_large` GitHub 响应超过 2 MB 限制
