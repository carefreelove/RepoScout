# Java Agent 框架对比：LangChain4j vs Spring AI Alibaba

## 一、项目定位与技术栈

### 1. LangChain4j (`langchain4j/langchain4j`)

**定位**：Java 版的 LangChain，一个独立的、框架无关的 LLM 应用开发库，强调"统一 API 抽象"。

**技术栈**：
- **语言/构建**：Java 8+（部分模块 Java 17），Maven 多模块工程
- **核心抽象**：`ChatLanguageModel`、`EmbeddingModel`、`ChatMemory`、`AiServices`（声明式接口）、`Tool`/`ToolSpecification`（函数调用）、`RetrievalAugmentor`（RAG）
- **Agent 能力**：通过 `AiServices` + `@Tool` 注解实现工具调用；`langchain4j-agentic` 模块（较新）提供多 Agent 编排
- **集成生态**：OpenAI、Anthropic、Gemini、Ollama、Azure OpenAI、Bedrock、Mistral 等 20+ 模型提供商；向量库（Pinecone、Milvus、Qdrant、pgvector、Elasticsearch 等）；Spring Boot Starter 官方提供
- **框架无关**：可脱离 Spring 使用，也可通过 `langchain4j-spring-boot-starter` 集成 Spring Boot

**使用方式示例**（声明式 AiService）：
```java
interface Assistant {
    @SystemMessage("You are a helpful assistant")
    String chat(@UserMessage String userMessage);
}

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)
    .tools(new CalculatorTool())
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .build();

String answer = assistant.chat("What is 2+2?");
```

**来源**：
- GitHub: https://github.com/langchain4j/langchain4j
- 官方文档: https://docs.langchain4j.dev/
- Agentic 模块: https://docs.langchain4j.dev/tutorials/agents

---

### 2. Spring AI Alibaba (`alibaba/spring-ai-alibaba`)

**定位**：阿里云基于 **Spring AI** 的增强实现，面向 Spring 生态，深度集成阿里云百炼（DashScope）、通义千问（Qwen）等模型，并提供 **Graph 多 Agent 编排**能力。

**技术栈**：
- **语言/构建**：Java 17+，Spring Boot 3.x，Maven
- **基础**：构建在 `spring-projects/spring-ai` 之上，复用其 `ChatClient`、`ChatModel`、`EmbeddingModel`、`VectorStore`、`Advisor` 等抽象
- **Agent 能力**：
  - `spring-ai-alibaba-graph`：基于 **StateGraph** 的工作流/多 Agent 编排（类似 LangGraph），支持节点、边、条件路由、状态持久化、Human-in-the-loop
  - `spring-ai-alibaba-starter-dashscope`：通义千问模型接入
  - 工具调用、RAG、MCP 支持
- **集成生态**：DashScope（Qwen-Max/Plus/Turbo、Qwen-VL、Qwen-Audio）、百炼平台、阿里云向量检索、Nacos 配置、Higress 网关等
- **强 Spring 绑定**：以 Spring Boot Starter 形式提供，依赖 Spring 容器与自动配置

**使用方式示例**（ChatClient + Graph）：
```java
@RestController
class ChatController {
    private final ChatClient chatClient;

    ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/chat")
    String chat(@RequestParam String msg) {
        return chatClient.prompt().user(msg).call().content();
    }
}
```

Graph 编排（多 Agent）：
```java
StateGraph graph = new StateGraph("agent-flow", stateFactory)
    .addNode("planner", node_async(plannerNode))
    .addNode("executor", node_async(executorNode))
    .addEdge(START, "planner")
    .addConditionalEdges("planner", edge_async(this::route), Map.of("exec", "executor", "end", END))
    .addEdge("executor", END)
    .compile();
```

**来源**：
- GitHub: https://github.com/alibaba/spring-ai-alibaba
- 官方文档: https://java2ai.com/
- Graph 文档: https://java2ai.com/docs/frameworks/graph-core/quick-start
- 底层 Spring AI: https://github.com/spring-projects/spring-ai

---

## 二、核心对比

| 维度 | LangChain4j | Spring AI Alibaba |
|---|---|---|
| **基础依赖** | 独立库，框架无关 | 依赖 Spring AI + Spring Boot 3 |
| **Java 版本** | Java 8/17 | Java 17+ |
| **模型接入** | 20+ 提供商，国际化 | 主打 DashScope/通义千问，兼顾 Spring AI 支持的模型 |
| **Agent 编排** | `AiServices` + `@Tool`；`langchain4j-agentic` 多 Agent | `StateGraph`（类 LangGraph）工作流编排，功能更完整 |
| **RAG** | `RetrievalAugmentor` + 多向量库 | Spring AI `VectorStore` + `Advisor` |
| **Spring 集成** | 官方 Starter，可选 | 原生 Spring Boot Starter，深度绑定 |
| **生态偏向** | 通用、跨云 | 阿里云生态（百炼、Nacos、Higress） |
| **学习曲线** | 中等，API 直观 | 需先理解 Spring AI 抽象 |
| **适用场景** | 非 Spring 项目、多模型切换、轻量集成 | Spring Boot 项目、需要复杂多 Agent 工作流、阿里云用户 |

---

## 三、选型建议

- **已有 Spring Boot 3 项目 + 使用阿里云/通义千问 + 需要复杂多 Agent 工作流** → **Spring AI Alibaba**（Graph 编排能力强）
- **非 Spring 项目、需要灵活切换多家模型、追求轻量声明式 API** → **LangChain4j**
- **两者可共存**：LangChain4j 提供 Spring Boot Starter，Spring AI 也可通过适配层调用；实际项目中可按模块选择。

---

## 四、参考来源汇总

1. LangChain4j GitHub — https://github.com/langchain4j/langchain4j
2. LangChain4j 官方文档 — https://docs.langchain4j.dev/
3. LangChain4j Agents 教程 — https://docs.langchain4j.dev/tutorials/agents
4. Spring AI Alibaba GitHub — https://github.com/alibaba/spring-ai-alibaba
5. Spring AI Alibaba 官网 — https://java2ai.com/
6. Spring AI Alibaba Graph 文档 — https://java2ai.com/docs/frameworks/graph-core/quick-start
7. Spring AI 官方 — https://github.com/spring-projects/spring-ai
8. Spring AI 文档 — https://docs.spring.io/spring-ai/reference/

> 注：两个项目迭代较快（尤其 Agent/Graph 模块），具体 API 以对应版本官方文档为准。
