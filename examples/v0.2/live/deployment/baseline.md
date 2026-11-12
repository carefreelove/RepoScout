# Java 后端 Agent 项目调研：聚焦 spring-ai-alibaba

## 一、Java 后端 Agent 项目概览

| 项目 | 定位 | 成熟度 | 备注 |
|---|---|---|---|
| **alibaba/spring-ai-alibaba** | Spring AI 的阿里生态实现，含 Graph/Agent 编排 | 活跃，1.0 前后迭代快 | 本次重点 |
| Spring AI (官方) | Spring 官方 AI 抽象层 | 稳定 | 基础依赖 |
| LangChain4j | Java 版 LangChain，Agent/Tool 支持完善 | 成熟 | 社区活跃 |
| Semantic Kernel Java | 微软 SK 的 Java 版 | 早期 | 生态偏 .NET |
| Agent-Flex / Solon-AI | 国产轻量 Agent 框架 | 小众 | 文档较少 |

---

## 二、spring-ai-alibaba 资料分类

### A. 官方文档（可信度高，但需注意版本漂移）

1. **GitHub 仓库 README + Wiki**
   - `https://github.com/alibaba/spring-ai-alibaba`
   - 含模块划分：`spring-ai-alibaba-core`、`spring-ai-alibaba-graph`、`spring-ai-alibaba-studio`、`spring-ai-alibaba-nl2sql` 等。
   - **注意**：README 中的依赖坐标随版本变化频繁（`1.0.0-M*` → `1.0.0.x`），务必以仓库 `pom.xml` 的 `<version>` 为准。

2. **官方文档站**
   - `https://java2ai.com/`（Spring AI Alibaba 官方文档）
   - 覆盖：快速开始、Graph 编排、多 Agent、Tool Calling、RAG、可观测性。
   - **文档滞后点**：Graph 的 API（如 `StateGraph`、`CompiledGraph`）在 M 版本间有破坏性变更，文档示例常落后于代码。

3. **示例仓库**
   - `spring-ai-alibaba-examples`（同组织下）
   - 含 `graph`、`chatbot`、`nl2sql`、`deepresearch` 等可运行 demo，是**最接近实测**的官方资料。

4. **阿里云百炼 / DashScope 文档**
   - 模型接入（qwen-plus/max、embedding）的 API Key 与 endpoint 配置说明。

### B. 社区实测 / 博客（需交叉验证）

- 掘金、CSDN、InfoQ 中文站有大量"Spring AI Alibaba 入门"文章，**质量参差**：
  - 常见问题：直接抄 README 的旧版本坐标，导致 `NoSuchMethodError`。
  - 有价值的：Graph 状态机调试经验、与 Nacos 集成的踩坑记录。
- B 站/YouTube 有部署演示视频，可作流程参考，但版本信息需自行核对。

### C. 需自行实测验证的关键点（文档未明确或易踩坑）

1. **版本矩阵**：Spring Boot 3.x + Spring AI 1.0.x + spring-ai-alibaba 的兼容组合，官方 BOM 是否覆盖。
2. **Graph 编译期 vs 运行期**：`StateGraph` 定义后 `compile()` 的行为、条件边（conditional edge）的路由函数签名。
3. **Tool Calling 与模型能力匹配**：qwen 系列对 function calling 的支持差异（部分模型不支持并行工具调用）。
4. **流式输出 + Graph**：SSE 在 Graph 节点间的透传是否完整。
5. **可观测性**：与 Micrometer / OpenTelemetry 的集成是否开箱可用。
6. **部署形态**：作为 Spring Boot 应用打包 vs 接入 `spring-ai-alibaba-studio` 做可视化调试。

---

## 三、建议的实测路径

```
1. 拉取 spring-ai-alibaba-examples 中 graph 示例
2. 配置 DashScope API Key（环境变量 DASHSCOPE_API_KEY）
3. mvn spring-boot:run 跑通单 Agent → 多 Agent 编排
4. 替换为本地 Ollama 模型验证解耦性
5. 压测流式接口，观察 Graph 节点耗时
```

---

## 四、结论

- **文档可信但需锁版本**：以 GitHub 仓库 tag + `pom.xml` 为准，文档站作流程参考。
- **实测优先看 examples 仓库**：比博客可靠，比文档新。
- **重点验证**：版本兼容矩阵、Graph API 稳定性、qwen 工具调用能力、流式透传。
- 若追求稳定生产，可对比 **LangChain4j**（API 更稳定、文档更系统）；若深度绑定阿里云生态，spring-ai-alibaba 是首选。

需要我进一步展开某一模块（如 Graph 编排的实测代码骨架、或与 LangChain4j 的对比表）吗？
