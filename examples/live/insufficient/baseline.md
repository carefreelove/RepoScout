# Java Agent 框架 QPS 基准核查：langchain4j/langchain4j

## 结论先行

**未确认。** 截至本次检索，**没有找到 langchain4j/langchain4j 官方或第三方发布的、可证明单机 1 万 QPS 的独立基准测试**。任何声称 langchain4j 单机可达 1 万 QPS 的说法，目前都缺乏可核验的公开证据。

---

## 一、检索范围与方法

针对以下来源进行了检索：

1. **GitHub 仓库 `langchain4j/langchain4j`**
   - README、Wiki、`docs/` 目录
   - Issues / Discussions 中关键词：`benchmark`、`QPS`、`throughput`、`performance`、`load test`
   - `langchain4j-benchmarks` 或类似模块是否存在
2. **官方文档站**（docs.langchain4j.dev）
3. **公开技术博客 / 会议材料**中提及 langchain4j 性能数字的内容
4. **JMH / Gatling / wrk 等基准工具**在 langchain4j 生态中的使用记录

---

## 二、核查结果

### 2.1 官方基准：不存在

- langchain4j 仓库**没有独立的 benchmark 模块**，也没有官方发布的 QPS/吞吐量报告。
- 官方文档聚焦于 API 用法、集成（OpenAI、Ollama、PGVector 等）、RAG、Agent/Tool 调用，**未提供任何性能基准数据**。
- 仓库内 Issues 中关于性能的讨论多为**个案调优**（如流式响应延迟、embedding 批处理），**不构成可复现的 QPS 基准**。

### 2.2 第三方独立基准：未找到可核验来源

- 未检索到以 langchain4j 为被测对象、公开测试方法（硬件规格、模型后端、并发模型、prompt 长度、是否 mock LLM）的独立基准报告。
- 网络上零散的"性能对比"多为**定性描述**或**未披露测试条件**，无法支撑"单机 1 万 QPS"这一具体数字。

### 2.3 为什么"1 万 QPS"本身需要谨慎解读

即使未来出现基准，也需区分被测对象：

| 场景 | 1 万 QPS 是否现实 | 说明 |
|---|---|---|
| **纯框架开销**（mock LLM，仅测 Agent 编排/工具调度/序列化） | 可能达到，取决于实现 | 此时测的是 Java 框架本身，与真实 LLM 无关 |
| **含真实 LLM 调用**（OpenAI/本地模型） | 单机 1 万 QPS 基本不现实 | 瓶颈在模型推理与网络 RTT，不在框架 |
| **本地小模型 + 批处理** | 需明确模型、量化、GPU 规格 | 数字强依赖硬件与模型 |

因此，"langchain4j 单机 1 万 QPS"若脱离**被测边界（是否含 LLM 推理）**，本身就是一个**定义不清的指标**。

---

## 三、可复现的验证建议

若需自行验证，建议按以下方式构建基准（这也是目前缺失的部分）：

1. **明确边界**：区分「框架编排开销」与「端到端含 LLM」两类基准。
2. **Mock LLM**：用固定延迟/零延迟的 stub ChatModel 测框架吞吐上限。
3. **工具链**：JMH（微基准）+ Gatling/wrk（端到端 HTTP）。
4. **披露条件**：CPU 核数、JVM 版本与 GC、堆大小、并发数、prompt/response token 长度、是否流式。
5. **报告 P50/P99 延迟与吞吐**，而非单一 QPS 数字。

---

## 四、总结

| 核查项 | 结果 |
|---|---|
| langchain4j 官方 QPS 基准 | ❌ 不存在 |
| 第三方独立 1 万 QPS 基准 | ❌ 未找到可核验来源 |
| "单机 1 万 QPS"可证明性 | ⚠️ **未确认**，且指标定义需先澄清（是否含 LLM 推理） |

**明确结论：资料不足，langchain4j 单机 1 万 QPS 的说法目前无法被公开资料证实。** 如需该数字，应自行按上述方法构建并公开可复现基准。
