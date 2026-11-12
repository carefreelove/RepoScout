# Java 开源 LLM Agent 框架调研：重点 langchain4j

## 一、Java 生态主流开源 LLM Agent 框架概览

| 框架 | 组织 | 定位 | Agent 能力 |
|---|---|---|---|
| **LangChain4j** | langchain4j 社区 | Java 版 LangChain，最活跃 | AI Services、Tools、Agentic 工作流 |
| **Spring AI** | VMware/Spring | Spring 生态集成 | Tool Calling、Advisors、MCP |
| **Semantic Kernel (Java)** | Microsoft | 多语言 SK 的 Java 版 | Planner、Plugins |
| **Agent-Flex / Embabel** | 社区 / Rod Johnson | JVM Agent 编排 | 工作流式 Agent |
| **Quarkus LangChain4j** | Quarkus | LangChain4j 的 Quarkus 扩展 | 同上 + 原生编译 |

其中 **LangChain4j** 是 Java 生态中功能最完整、社区最活跃的 Agent 框架，下面重点调研。

---

## 二、LangChain4j 调研

### 1. 项目基本信息（源码依据）

- 仓库：`https://github.com/langchain4j/langchain4j`
- 许可证：Apache-2.0（见仓库根目录 `LICENSE`）
- 构建：Maven 多模块，根 `pom.xml` 中 `groupId=dev.langchain4j`
- 版本线：`1.x`（2025 年发布 1.0 GA），此前为 `0.x`

### 2. Maven 依赖（依据：官方 README / 各模块 pom.xml）

**核心依赖：**

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j</artifactId>
    <version>1.0.0</version> <!-- 以 Maven Central 最新为准 -->
</dependency>
```

**常用扩展模块（artifactId 均以 `langchain4j-` 前缀，见仓库 `langchain4j-*` 目录）：**

| 能力 | artifactId |
|---|---|
| OpenAI | `langchain4j-open-ai` |
| Ollama（本地模型） | `langchain4j-ollama` |
| Anthropic Claude | `langchain4j-anthropic` |
| 通义/DeepSeek 等 OpenAI 兼容 | 用 `langchain4j-open-ai` 改 baseUrl |
| 向量库（PGVector） | `langchain4j-pgvector` |
| 向量库（Milvus/Chroma 等） | `langchain4j-milvus` / `langchain4j-chroma` |
| Spring Boot Starter | `langchain4j-spring-boot-starter` |
| Quarkus 扩展 | `quarkus-langchain4j-*`（独立仓库 `quarkus-langchain4j`） |

> 依据：仓库 `langchain4j-open-ai/pom.xml`、`langchain4j-spring-boot-starter/pom.xml` 等模块均声明 `groupId=dev.langchain4j`，父 POM 为 `langchain4j-parent`。

### 3. Agent 相关核心 API（源码依据）

LangChain4j 的 Agent 能力主要通过 **AI Services + Tools（Function Calling）** 实现，源码位于 `langchain4j/src/main/java/dev/langchain4j/service/`：

- **`AiServices`**（`dev.langchain4j.service.AiServices`）：声明式接口，把 Java 接口方法映射为 LLM 调用，支持 `tools(...)` 注册工具。
- **`@Tool`** 注解（`dev.langchain4j.agent.tool.Tool`）：标注 Java 方法为可被 LLM 调用的工具，源码路径 `langchain4j-core/src/main/java/dev/langchain4j/agent/tool/Tool.java`。
- **`ToolSpecification` / `ToolExecutor`**（`dev.langchain4j.agent.tool` 包）：工具描述与执行抽象。
- **`@SystemMessage` / `@UserMessage` / `@MemoryId`**：`dev.langchain4j.service` 包下的注解，用于提示词与记忆管理。
- **Agentic 工作流**：1.x 引入 `dev.langchain4j.agentic` 模块（仓库目录 `langchain4j-agentic`），支持 `@Agent`、`@Sequence`、`@Parallel`、`@Loop`、`@Conditional` 等编排注解，是官方对"Agent 框架"的正式支持。

**最小 Agent 示例（依据官方 README 与 `AiServices` 用法）：**

```java
interface Assistant {
    @SystemMessage("你是一个会使用工具的助手")
    String chat(String userMessage);
}

class Calculator {
    @Tool("计算两个数之和")
    double add(double a, double b) { return a + b; }
}

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)          // 如 OpenAiChatModel
    .tools(new Calculator())
    .build();

String answer = assistant.chat("3 加 5 等于几？");
```

### 4. 关键能力对照（源码/文档依据）

| 能力 | 支持情况 | 依据 |
|---|---|---|
| Function/Tool Calling | ✅ | `dev.langchain4j.agent.tool.Tool`、`ToolSpecification` |
| 多轮记忆 | ✅ | `dev.langchain4j.memory.ChatMemory`、`MessageWindowChatMemory` |
| RAG | ✅ | `langchain4j-easy-rag`、`EmbeddingStore`、`ContentRetriever` |
| 结构化输出 | ✅ | `AiServices` 返回 POJO，内部用 JSON schema |
| 流式输出 | ✅ | `StreamingChatLanguageModel`、`TokenStream` |
| Agentic 编排 | ✅（1.x） | `langchain4j-agentic` 模块 |
| MCP 协议 | ✅ | `langchain4j-mcp` 模块 |
| 可观测性 | ✅ | `langchain4j` 集成 Micrometer / OpenTelemetry 模块 |

### 5. 生态与活跃度（可核验）

- GitHub Stars 数量级：**7k+**（截至 2025 年，见仓库首页 badge）。
- 发布节奏：Maven Central 上 `dev.langchain4j:langchain4j` 每月多次发布（可在 `https://central.sonatype.com/artifact/dev.langchain4j/langchain4j` 核验）。
- 官方文档：`https://docs.langchain4j.dev/`，含 "Tutorials → Agents"、"AI Services"、"Tools" 章节。
- Spring Boot 官方 starter：`langchain4j-spring-boot-starter`，另有 `langchain4j-spring-boot-starter-*` 系列（如 `-open-ai`）。

---

## 三、选型建议

1. **纯 Java / 需要最大灵活性** → **LangChain4j**（模块化、无框架绑定、Agentic 模块已 GA）。
2. **Spring Boot 项目** → **Spring AI** 或 **LangChain4j + spring-boot-starter**（后者生态更广、模型适配更多）。
3. **Quarkus / 原生镜像** → **quarkus-langchain4j**。
4. **需要微软生态/多语言统一** → **Semantic Kernel Java**（但 Java 版活跃度低于 LangChain4j）。

**结论**：若目标是"Java 开源 LLM Agent 框架"，**LangChain4j 是当前首选**——Apache-2.0、模块化 Maven 依赖、原生 `@Tool` + `AiServices` + `langchain4j-agentic` 编排，且与 Spring/Quarkus 均有官方集成。

---

## 四、核验清单（供你自行验证）

- [ ] `https://github.com/langchain4j/langchain4j` → 查看 `LICENSE`、根 `pom.xml` 的 `groupId`
- [ ] `https://central.sonatype.com/artifact/dev.langchain4j/langchain4j` → 确认最新版本
- [ ] 仓库目录 `langchain4j-agentic/` → 确认 Agentic 编排注解源码
- [ ] `langchain4j-core/src/main/java/dev/langchain4j/agent/tool/Tool.java` → 确认 `@Tool` 定义
- [ ] `https://docs.langchain4j.dev/tutorials/agents` → 官方 Agent 教程

如需，我可以进一步给出 **LangChain4j Agentic 模块的完整可运行示例**（含 `@Sequence`/`@Loop` 编排）或 **与 Spring AI 的逐项对比表**。
