# Java Agent 框架对比：LangChain4j vs Spring AI Alibaba

## 一、项目定位与技术栈

### 1. LangChain4j (`langchain4j/langchain4j`)

**定位**：Java 生态的 LLM 应用开发框架，灵感来自 Python 的 LangChain，目标是提供统一的 API 抽象，屏蔽不同 LLM 提供商和向量库的差异。

**技术栈**：
- **语言/构建**：Java 8+（部分模块要求 Java 17），Maven 多模块工程
- **核心抽象**：`ChatLanguageModel`、`EmbeddingModel`、`EmbeddingStore`、`ChatMemory`、`AiServices`（声明式接口）
- **Agent 能力**：`AiServices` + `@Tool` 注解实现工具调用（Function Calling）；`langchain4j-agentic` 模块支持多 Agent 编排（顺序、并行、循环、条件路由）
- **RAG 支持**：内置文档加载器、切分器、EmbeddingStore 集成（Pinecone、Milvus、PgVector、Elasticsearch 等）
- **集成生态**：OpenAI、Anthropic、Azure OpenAI、Ollama、Google Gemini、Bedrock、DashScope 等
- **Spring 集成**：`langchain4j-spring-boot-starter`（社区维护，非官方主推）

**使用方式（示例）**：
```java
interface Assistant {
    @SystemMessage("You are a helpful assistant")
    String chat(@UserMessage String userMessage);
}

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(OpenAiChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .build())
    .tools(new CalculatorTool())
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .build();

String answer = assistant.chat("What is 2+2?");
```

**特点**：框架中立、不绑定 Spring，适合纯 Java 项目或非 Spring 技术栈；抽象层次高，学习曲线相对平缓。

---

### 2. Spring AI Alibaba (`alibaba/spring-ai-alibaba`)

**定位**：阿里云基于 **Spring AI** 构建的 Agentic AI 框架，深度集成阿里云百炼（DashScope）通义千问系列模型，同时兼容 OpenAI 等主流模型。是 Spring 官方 AI 生态在中国区的增强实现。

**技术栈**：
- **语言/构建**：Java 17+，Spring Boot 3.x，Maven
- **底层依赖**：Spring AI（`org.springframework.ai`）核心抽象（`ChatClient`、`ChatModel`、`EmbeddingModel`、`VectorStore`）
- **Agent 能力**：
  - **Graph 多 Agent 编排**：基于状态图（StateGraph）的 Agent 工作流，支持节点、边、条件路由、并行、人工介入（Human-in-the-loop）
  - **ReactAgent**：ReAct 模式的自主 Agent
  - **工具调用**：`@Tool` 注解 + Spring Bean 注入
  - **MCP 支持**：集成 Model Context Protocol
- **RAG 支持**：基于 Spring AI 的 `VectorStore` 抽象，集成阿里云百炼知识库、AnalyticDB、Milvus 等
- **可观测性**：集成 Spring Boot Actuator、Micrometer、ARMS（阿里云应用实时监控）
- **模型生态**：DashScope（通义千问 Qwen-Max/Plus/Turbo、Qwen-VL、Qwen-Audio）、OpenAI 兼容接口

**使用方式（示例）**：
```java
@RestController
public class ChatController {
    private final ChatClient chatClient;

    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("You are a helpful assistant")
            .defaultTools(new DateTimeTools())
            .build();
    }

    @GetMapping("/chat")
    public String chat(@RequestParam String message) {
        return chatClient.prompt().user(message).call().content();
    }
}
```

**Graph Agent 编排示例**：
```java
StateGraph graph = new StateGraph("my-agent", stateFactory)
    .addNode("agent", node_async(new ReactAgent(...)))
    .addNode("tool", node_async(new ToolNode(...)))
    .addEdge(START, "agent")
    .addConditionalEdges("agent", edge_async(state -> 
        state.value("hasToolCall").equals(true) ? "tool" : END))
    .addEdge("tool", "agent")
    .compile();
```

**特点**：Spring 原生体验（依赖注入、配置管理、Actuator），面向企业级生产环境；Graph 编排能力强，适合复杂多 Agent 工作流；与阿里云生态深度绑定。

---

## 二、核心对比

| 维度 | LangChain4j | Spring AI Alibaba |
|------|-------------|-------------------|
| **基础框架** | 自研抽象，框架中立 | 基于 Spring AI + Spring Boot 3 |
| **Java 版本** | Java 8/17+ | Java 17+ |
| **Spring 依赖** | 可选（starter 社区维护） | 强依赖（Spring 原生） |
| **Agent 编排** | `AiServices` + `langchain4j-agentic`（顺序/并行/循环/条件） | StateGraph 状态图 + ReactAgent + 条件路由 + 人工介入 |
| **工具调用** | `@Tool` 注解 | `@Tool` 注解 + Spring Bean |
| **MCP 支持** | 有（`langchain4j-mcp`） | 有（原生集成） |
| **模型生态** | 极广（OpenAI/Anthropic/Gemini/Ollama/Bedrock/DashScope…） | 以 DashScope 为主，兼容 OpenAI 接口 |
| **RAG** | 完整（加载器/切分器/多种 VectorStore） | 基于 Spring AI VectorStore + 百炼知识库 |
| **可观测性** | 基础（日志、监听器） | 强（Actuator/Micrometer/ARMS） |
| **适用场景** | 通用 Java 应用、非 Spring 项目、多模型切换 | Spring Boot 企业应用、阿里云用户、复杂 Agent 工作流 |

---

## 三、选型建议

- **选 LangChain4j**：项目非 Spring 技术栈、需要广泛的多模型/多向量库支持、希望框架轻量中立、需要声明式 `AiServices` 快速开发。
- **选 Spring AI Alibaba**：已有 Spring Boot 3 企业应用、使用阿里云百炼/通义千问、需要 Graph 状态图编排复杂多 Agent 工作流、需要完善的可观测性与生产级治理。

---

## 四、来源

1. **LangChain4j 官方仓库**：https://github.com/langchain4j/langchain4j
2. **LangChain4j 官方文档**：https://docs.langchain4j.dev/
3. **LangChain4j Agentic 模块文档**：https://docs.langchain4j.dev/tutorials/agents
4. **Spring AI Alibaba 官方仓库**：https://github.com/alibaba/spring-ai-alibaba
5. **Spring AI Alibaba 官方文档**：https://java2ai.com/
6. **Spring AI 官方文档**：https://docs.spring.io/spring-ai/reference/
7. **Spring AI Alibaba Graph 文档**：https://java2ai.com/docs/frameworks/graph-core/overview

> 注：两个项目迭代较快，具体 API 与模块名称请以官方最新文档为准。
