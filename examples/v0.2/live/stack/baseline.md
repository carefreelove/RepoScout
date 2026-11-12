# LangChain4j 调研报告

## 一、结论先行

**LangChain4j 是当前 Java 生态中最成熟、最活跃的开源 LLM Agent 框架**，支持 Agent（工具调用）、RAG、Memory、多模型接入等完整能力。以下给出依赖坐标与源码依据。

---

## 二、LangChain4j 基本信息

| 项目 | 内容 |
|---|---|
| 仓库 | https://github.com/langchain4j/langchain4j |
| 官网 | https://docs.langchain4j.dev |
| License | Apache-2.0 |
| 语言 | Java 17+ |
| 构建 | Maven（多模块） |
| 当前稳定版本 | 1.x（2025 年发布 1.0 GA） |

---

## 三、依赖坐标（Maven）

### 1. 核心 BOM（推荐统一版本管理）

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>dev.langchain4j</groupId>
      <artifactId>langchain4j-bom</artifactId>
      <version>1.0.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### 2. 核心依赖

```xml
<!-- 核心 API：ChatModel、EmbeddingModel、AiServices 等 -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j</artifactId>
</dependency>

<!-- 高层 Agent 抽象：AiServices、@Tool、@MemoryId 等 -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-core</artifactId>
</dependency>
```

### 3. 模型接入（按需）

```xml
<!-- OpenAI / 兼容 OpenAI 协议的模型（DeepSeek、Qwen、Ollama 等） -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-open-ai</artifactId>
</dependency>

<!-- Ollama 本地模型 -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-ollama</artifactId>
</dependency>

<!-- Anthropic Claude -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-anthropic</artifactId>
</dependency>

<!-- 通义千问 DashScope -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-dashscope</artifactId>
</dependency>
```

### 4. RAG / 向量库 / 工具

```xml
<!-- 文档解析 -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-document-parser-apache-pdfbox</artifactId>
</dependency>

<!-- 向量库（示例：内存版 / PGVector / Milvus / Qdrant） -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-embeddings-all-minilm-l6-v2</artifactId>
</dependency>
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-pgvector</artifactId>
</dependency>

<!-- Spring Boot 集成 -->
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-spring-boot-starter</artifactId>
</dependency>
```

> 完整模块清单见仓库根目录 `pom.xml` 的 `<modules>` 段，以及 `langchain4j-bom/pom.xml`。

---

## 四、Agent 能力源码依据

### 1. Agent 的核心抽象：`AiServices`

**源码路径**：`langchain4j/src/main/java/dev/langchain4j/service/AiServices.java`

```java
public interface Assistant {
    String chat(String userMessage);
}

Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(model)
    .tools(new Calculator())   // 注册工具 → 具备 Agent 能力
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .build();
```

`AiServices` 是 LangChain4j 的"Agent 编排层"，负责：
- 解析接口方法 → 构造 Prompt
- 注入 `@Tool` 方法 → 生成 function-calling schema
- 处理工具调用循环（LLM 返回 tool_call → 执行 → 回填 → 再请求）
- 管理 `ChatMemory`

### 2. 工具调用（Function Calling）实现

**源码路径**：
- `langchain4j-core/src/main/java/dev/langchain4j/agent/tool/ToolSpecification.java`
- `langchain4j-core/src/main/java/dev/langchain4j/agent/tool/ToolSpecifications.java`
- `langchain4j/src/main/java/dev/langchain4j/service/tool/ToolService.java`
- `langchain4j/src/main/java/dev/langchain4j/service/DefaultAiServices.java`（工具执行循环）

`@Tool` 注解定义在 `dev.langchain4j.agent.tool.Tool`，`ToolSpecifications.toolSpecificationsFrom(Object)` 通过反射把 Java 方法转成 JSON Schema 供模型调用。

### 3. 工具执行循环（Agent Loop）

**源码路径**：`langchain4j/src/main/java/dev/langchain4j/service/DefaultAiServices.java`

关键逻辑：当 `ChatResponse` 中 `aiMessage.hasToolExecutionRequests()` 为 true 时，遍历 `ToolExecutionRequest`，调用 `ToolService.execute()`，把 `ToolExecutionResultMessage` 追加到消息列表，再次调用模型，直到模型返回纯文本。这就是标准的 ReAct 式 Agent 循环。

### 4. 内置 Agent 模式

- **`langchain4j-agentic`**（1.x 新增模块）：多 Agent 协作、Supervisor、Workflow 编排
- **`langchain4j-mcp`**：MCP（Model Context Protocol）客户端，可接入外部工具服务器
- **`langchain4j-experimental-sql`**：Text-to-SQL Agent

---

## 五、最小可运行 Agent 示例

```java
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.agent.tool.Tool;

public class AgentDemo {

    static class WeatherTools {
        @Tool("查询指定城市的当前天气")
        String getWeather(String city) {
            return city + " 今天晴，25°C";
        }
    }

    interface WeatherAgent {
        String ask(String question);
    }

    public static void main(String[] args) {
        var model = OpenAiChatModel.builder()
            .apiKey(System.getenv("OPENAI_API_KEY"))
            .modelName("gpt-4o-mini")
            .build();

        WeatherAgent agent = AiServices.builder(WeatherAgent.class)
            .chatLanguageModel(model)
            .tools(new WeatherTools())
            .build();

        System.out.println(agent.ask("北京天气怎么样？"));
    }
}
```

---

## 六、与其他 Java 生态框架对比

| 框架 | 定位 | Agent 能力 | 活跃度 |
|---|---|---|---|
| **LangChain4j** | 通用 LLM 应用框架 | ✅ 完整（工具、MCP、多 Agent） | ⭐⭐⭐⭐⭐ |
| **Spring AI** | Spring 官方 AI 抽象 | ✅ 有（Advisor + Tool Calling） | ⭐⭐⭐⭐ |
| **Semantic Kernel Java** | 微软 SK 的 Java 移植 | ✅ 有（Planner） | ⭐⭐（Java 版滞后） |
| **Agent-Flex / JManus** | 阿里系 Agent 框架 | ✅ 专注 Agent | ⭐⭐⭐ |

**选型建议**：
- 需要**最全的模型/向量库适配 + 成熟 Agent 抽象** → LangChain4j
- 深度 Spring 项目、偏好官方支持 → Spring AI（也可与 LangChain4j 共存）
- 需要**可视化多 Agent 编排** → 关注 `langchain4j-agentic` 或 JManus

---

## 七、验证依赖/源码的方法

```bash
# 1. 克隆仓库
git clone https://github.com/langchain4j/langchain4j.git
cd langchain4j

# 2. 查看所有模块
grep -A200 "<modules>" pom.xml

# 3. 查看 BOM 中所有可引入的 artifact
cat langchain4j-bom/pom.xml | grep artifactId

# 4. 定位 Agent 核心代码
find . -name "AiServices.java" -o -name "ToolService.java" -o -name "DefaultAiServices.java"

# 5. 查看 Maven Central 上的发布版本
# https://central.sonatype.com/artifact/dev.langchain4j/langchain4j
```

---

## 八、注意事项

1. **版本**：1.0 GA 之前 API 变动较大，务必锁定版本（推荐 1.x 最新 patch）。
2. **Java 版本**：1.x 要求 **Java 17+**。
3. **OpenAI 兼容层**：`langchain4j-open-ai` 可对接 DeepSeek、Qwen、Moonshot、Ollama 等任何兼容 OpenAI 协议的服务，只需改 `baseUrl`。
4. **Agent 循环成本**：工具调用会多次请求 LLM，注意 token 消耗与超时配置（`maxSequentialToolsInvocations` 等参数在 `DefaultAiServices` 中可调）。

如需进一步深入某个模块（如 MCP 集成、多 Agent 编排、RAG 流水线），可以继续指定方向。
