# Java 后端 Agent 项目调研：聚焦 spring-ai-alibaba

## 一、可用的 Java Agent 项目概览

| 项目 | 定位 | 成熟度 |
|---|---|---|
| **alibaba/spring-ai-alibaba** | Spring AI 的阿里系实现，集成 DashScope/通义千问，含 Graph 编排 | 活跃，1.x 已发布 |
| **spring-projects/spring-ai** | 官方 Spring AI，Agent 能力较基础 | 稳定 |
| **langchain4j** | Java 版 LangChain，Agent/Tool 支持完善 | 成熟 |
| **agents-flex** | 国产 Java Agent 框架 | 较新 |
| **Solon-AI** | 轻量级 Java AI 框架 | 小众 |

---

## 二、spring-ai-alibaba 资料分类

### 📄 文档类（官方/权威，可直接参考）

1. **官方 GitHub 仓库 README**
   - `https://github.com/alibaba/spring-ai-alibaba`
   - 含模块划分、快速开始、版本兼容矩阵（Spring Boot 3.x / Spring AI 1.0.x）

2. **官方文档站**
   - `https://java2ai.com`（Spring AI Alibaba 官方文档）
   - 覆盖：ChatModel 接入、Function Calling、**Graph 多智能体编排**、RAG、Observability

3. **示例仓库**
   - `spring-ai-alibaba/examples` 目录
   - `spring-ai-alibaba-graph-example`：多 Agent 工作流示例

4. **阿里云百炼 / DashScope 文档**
   - API Key 申请、模型列表、计费说明

5. **Spring AI 官方文档**（底层依赖）
   - `https://docs.spring.io/spring-ai/reference/`

### 🧪 实测类（社区经验，需自行验证）

- 掘金/CSDN 上的"Spring AI Alibaba 接入通义千问实战"系列文章
- B 站/YouTube 的 Graph 编排演示视频
- GitHub Issues 中的部署踩坑记录（版本冲突、流式响应、Tool 调用失败等）
- 各公司技术博客的落地案例（多为 2024 下半年后）

> ⚠️ 实测资料时效性强，**版本号必须核对**——1.0.0-M 系列与 1.0.x 正式版 API 差异较大。

---

## 三、部署要点（文档 + 实测综合）

### 1. 环境要求
- JDK 17+
- Spring Boot 3.3+
- Maven 3.8+

### 2. 依赖引入（以 1.0.x 为例）
```xml
<dependency>
  <groupId>com.alibaba.cloud.ai</groupId>
  <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
  <version>1.0.0.2</version>
</dependency>
```

### 3. 配置
```yaml
spring:
  ai:
    dashscope:
      api-key: ${DASHSCOPE_API_KEY}
      chat:
        options:
          model: qwen-plus
```

### 4. 最小 Agent 示例
```java
@RestController
public class ChatController {
    private final ChatClient chatClient;
    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("你是一个助手")
            .defaultTools(new WeatherTools())
            .build();
    }
    @GetMapping("/chat")
    public String chat(@RequestParam String q) {
        return chatClient.prompt().user(q).call().content();
    }
}
```

### 5. Graph 多智能体编排（核心亮点）
- 使用 `StateGraph` 定义节点（Agent/工具/条件分支）
- 支持 `CompiledGraph` 流式执行
- 参考 `spring-ai-alibaba-graph-example` 中的 ReAct、Routing 模式

---

## 四、实测常见坑（来自社区反馈，需验证）

| 问题 | 现象 | 建议 |
|---|---|---|
| 版本冲突 | Spring AI 与 Alibaba starter 版本不匹配导致 Bean 缺失 | 严格按官方兼容矩阵选版本 |
| 流式响应中断 | SSE 超时或编码问题 | 配置 `spring.mvc.async.request-timeout` |
| Tool 调用参数解析失败 | JSON Schema 不匹配 | 用 `@ToolParam` 明确描述 |
| Graph 状态序列化 | 复杂对象无法 checkpoint | 状态类实现 `Serializable` |
| DashScope 限流 | 429 错误 | 配置重试 + 降级 |

---

## 五、建议的调研路径

1. **先读文档**：java2ai.com 的 Quick Start + Graph 章节（1~2 小时）
2. **跑通示例**：clone examples，配置 API Key，跑 `graph-example`
3. **对照实测**：搜索"spring-ai-alibaba 1.0.x 踩坑"，重点看 2025 年后的文章
4. **验证关键点**：Tool Calling、流式输出、Graph 条件路由三项必须自测
5. **生产评估**：Observability（Micrometer）、限流、多模型切换

---

## 六、需要我进一步做什么？

- 帮你**拉取官方文档的具体章节内容**并整理成笔记？
- 对比 **spring-ai-alibaba vs langchain4j** 的 Agent 能力矩阵？
- 给出一个**可运行的最小 Graph 多 Agent 项目骨架**？

告诉我方向，我可以继续深入。
